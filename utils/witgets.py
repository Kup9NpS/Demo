# coding=utf-8
import urllib, re
from django import forms
from django.core.files import File
from django.db import models
import phonenumbers
from django.core import validators
from phonenumbers.phonenumberutil import NumberParseException
from django.core.exceptions import ValidationError
from sorl.thumbnail import ImageField


def urlencodenonascii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


def iritouri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlencodenonascii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )


class JasnyImageWidget(forms.FileInput):
    existing = '<img src="{url}" alt="{name}" width="{width}" height="{height}">'

    html = """\
           <br>
           <div class="fileinput fileinput-{state}" data-provides="fileinput">
             <div class="fileinput-preview thumbnail" data-trigger="fileinput" style="width: {width}px; height: {height}px;">
             {image}
             </div>
               <div>
                 <span class="btn btn-default btn-file">
                 <span class="fileinput-new">Выберите изображение</span>
                 <span class="fileinput-exists">Изменить</span>
                 <input type="file" name="{name}" accept="images/*"></span>
                 <input type="hidden" id="jasny-deleted" name="{name}-deleted" value="0">
                 <input type="hidden" id="jasny-url" name="{name}-url" value="">
                 <a href="#" id="a-jasny-deleted" class="btn btn-default fileinput-exists" data-dismiss="fileinput">Удалить</a>
               </div>
           </div>
           """

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        state = 'exists' if value else 'new'
        width = attrs.get('width', None) or 150
        height = attrs.get('width', None) if value else 150
        if isinstance(value, str):
            value = value
        elif isinstance(value, unicode):
            value = value
        elif isinstance(value, File):
            if hasattr(value, 'url'):
                value = value.url
            else:
                value = value
        else:
            value = None
        existing = self.existing.format(url=value, name=name, width=width, height=height) if value else ''
        return self.html.format(state=state, width=width, height=height, image=existing, name=name)

    def value_from_datadict(self, data, files, name):
        # del_query = unicode(name+'-deleted', "utf-8")
        # if del_query in data:
        #     deleted = bool(int(data[del_query]))
        #     # print deleted
        # else:
        #     deleted = False

        url_query = unicode(name+'-url', "utf-8")
        if url_query in data:
            url = data[url_query]
            if url == '':
                url = None
        else:
            url = None

        file = files.get(name, None)

        if not file and not url:
            return False
        if not file and url:
            print (url)
            url = iritouri(u"%s" % url)
            print (url)
            parsed_link = urlparse.urlsplit(url)
            parsed_link = parsed_link._replace(path=urllib.quote(parsed_link.path.encode('utf8')))
            encoded_link = parsed_link.geturl()

            result = urllib.urlretrieve(encoded_link)
            file = File(open(result[0]))
        return file


class JasnyImageField(forms.ImageField):
    widget = JasnyImageWidget


class JasnyImageModelField(ImageField):
    def formfield(self, **kwargs):
        defaults = {'form_class': JasnyImageField}
        defaults.update(kwargs)
        return super(JasnyImageModelField, self).formfield(**defaults)


# CUSTOM PHONE FIELD
#
#
def to_standart(value):
    try:
        x = phonenumbers.parse(value, "RU")
        phone_number = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        return value
    return phone_number


def validate_russian_phonenumber(value):
    try:
        x = phonenumbers.parse(value, "RU")
    except NumberParseException:
        raise ValidationError('Похоже, что это неправильный номер телефона')


class PhoneNumberDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))
        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = to_standart(value)


class MyPhoneField(models.Field):

    description = "Номер телефона"
    descriptor_class = PhoneNumberDescriptor
    default_validators = [validate_russian_phonenumber]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 128)
        super(MyPhoneField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))

    def get_internal_type(self):
        return 'CharField'

    def contribute_to_class(self, cls, name):
        super(MyPhoneField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.CharField,
        }
        defaults.update(kwargs)
        return super(MyPhoneField, self).formfield(**defaults)
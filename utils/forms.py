# coding=utf-8
from django import forms


class BootstrapForm(forms.Form):
    def as_div(self):
        return self._html_output(
            normal_row=u'<div class="form-group" %(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row=u'<div class="error">%s</div>',
            row_ender=u'</div>',
            help_text_html=u'<div class="help-text">%s</div>',
            errors_on_separate_row=False)


class BootstrapModelForm(forms.ModelForm):
    def as_div(self):
        return self._html_output(
            normal_row=u'<div class="form-group" %(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row=u'<div class="error">%s</div>',
            row_ender=u'</div>',
            help_text_html=u'<div class="help-text">%s</div>',
            errors_on_separate_row=False)
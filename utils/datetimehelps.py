# coding=utf-8
import datetime
from django.utils import timezone

_months_parent = [u'Января', u'Февраля',
                  u'Марта', u'Апреля', u'Мая',
                  u'Июня', u'Июля', u'Августа',
                  u'Сентября', u'Октября', u'Ноября', u'Декабря']

_months = [u'Январь', u'Февраль',
           u'Март', u'Апрель', u'Май',
           u'Июнь', u'Июль', u'Август',
           u'Сентябрь', u'Октябрь', u'Ноябрь', u'Декабрь']

_days = [u'Понедельник', u'Вторник', u'Среда', u'Четверг', u'Пятница', u'Суббота', u'Воскресенье']


class DateTime(object):

    @classmethod
    def now(cls):
        return timezone.now()

    @classmethod
    def time(cls):
        return DateTime.now().time()

    @classmethod
    def date(cls):
        return DateTime.now().date()


class BeautifulDateTime(object):
    @classmethod
    def make_instance(cls, d):
        if isinstance(d, datetime.time):
            return cls(time=d)
        if isinstance(d, datetime.date):
            return cls(date=d)
        if isinstance(d, datetime.datetime):
            return cls(datetime=d)
        return cls()

    def __init__(self, date=None, time=None, datetime_=None):
        if date:
            assert isinstance(date, datetime_.date)
        if time:
            assert isinstance(time, datetime_.time)
        if datetime_:
            assert isinstance(datetime_, datetime.datetime)
        assert any((date, time, datetime_)) and not all((date, time, datetime_))
        self._date = date
        self._time = time
        self._datetime = datetime_

    def _get_time(self):
        if self._time:
            return self._time
        if self._datetime:
            return self._datetime.time()
        raise ValueError('No time specified')

    def _get_date(self):
        if self._date:
            return self._date
        if self._datetime:
            return self._datetime.date()
        raise ValueError('No date specified')

    def _get_datetime(self):
        if self._datetime:
            return self._datetime
        if self._date and self._time:
            return datetime.datetime.combine(self._date, self._time)
        raise ValueError('No datetime specified')

    def day(self):
        return str(self._get_date().day)

    def day_name(self):
        return _days[self._get_date().weekday()]

    def month(self):
        return str(self._get_date().month)

    def month_name(self, parent=False):
        months = _months_parent if parent else _months
        return months[self._get_date().month - 1]

    def time(self):
        return u'{}:{}'.format(self._get_time().hour,
                               u'0' * (2 - len(str(self._get_time().minute))) + str(self._get_time().minute))

    def day_month(self):
        return u'{} {}'.format(self.day(), self.month_name(True).lower())


class DateTimeHelper(object):
    def __init__(self, datetime_):
        self._datetime = datetime_
        self.beautiful = BeautifulDateTime(datetime_=datetime_)

    def today(self):
        return self._datetime.date() == datetime.date.today()

    def tommorow(self):
        return self._datetime.date() == datetime.date.today() + datetime.timedelta(days=1)

    def yesterday(self):
        return self._datetime.date() == datetime.date.today() - datetime.timedelta(days=1)


class GameDateTimeHelper(DateTimeHelper):
    def __init__(self, game):
        self._duration = game.duration()
        super(GameDateTimeHelper, self).__init__(game.datetime())

    def passed(self):
        return self.end() < datetime.datetime.now()

    def now(self):
        return self._datetime <= datetime.datetime.now() <= self.end()

    def soon(self):
        return self._datetime > datetime.datetime.now() and \
               self._datetime - datetime.datetime.now() <= datetime.timedelta(hours=1)

    def end(self):
        return self._datetime + datetime.timedelta(minutes=self._duration)

    def can_subscribe(self):
        return not self.soon() and self._datetime > datetime.datetime.now()


def last_time_format(last_time):
    if DateTimeHelper(last_time).today():
        date = u'сегодня'
    elif DateTimeHelper(last_time).yesterday():
        date = u'вчера'
    else:
        date = BeautifulDateTime(datetime_=last_time).day_month()
    date += u' в ' + BeautifulDateTime(datetime_=last_time).time()
    return date


def between(value, start, end):
    return start <= value <= end
import re

from rest_framework.serializers import ValidationError


class UrlValidator:
    """Кастомный валидатор, для проверки поля url модели Lesson на принадлежность к определённому сайту."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        if url and not url.startswith('https://www.youtube.com/'):
            raise ValidationError('Можно указывать ссылку только с сайта http://www.youtube.com/')

    # def __call__(self, value):  # другой вариант записи метода __call__
    #     regular_expression = re.compile('https://youtube.com/')
    #     tmp_value = dict(value).get(self.field)
    #     if not bool(regular_expression.match(tmp_value)):
    #         raise ValidationError('Можно указывать ссылку только с сайта http://www.youtube.com/')

from django.core.validators import RegexValidator


def get_phone_regex_validator():
    return RegexValidator(
        regex=r'^7\d{10}$',
        message='Wrong phone number format. Valid phone number needs to be in the following format: 7XXXXXXXXXX.'
    )

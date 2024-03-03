from django.core.exceptions import ValidationError


def validate_username(self, value):
    if value.lower() == 'me':
        raise ValidationError(
            'Недопустимое имя пользователя.'
        )
    return value

from django.core.exceptions import ValidationError
import re

class containLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                'your password should contain letter',
                code='password_no_letter'
            )

    def get_help_text(self):
        return 'Your password should contain one letter min'


class containDigitValidator:
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                'Your password should contain at least one number',
                code='password_no_number'
            )
    def get_help_text(self):
        return 'Your password should contain at least one number'
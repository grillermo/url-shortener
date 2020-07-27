from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os

def secure_compare(actual, expected):
    """
    Returns True if the two strings are equal, False otherwise
    The time taken is dependent on the number of characters provided
    instead of the number of characters that match.
    When we upgrade to Python 2.7.7 or newer, we should use hmac.compare_digest
    instead.
    """
    actual_len   = len(actual)
    expected_len = len(expected)
    result = actual_len ^ expected_len
    if expected_len > 0:
        for i in range(actual_len):
            result |= ord(actual[i]) ^ ord(expected[i % expected_len])
    return result == 0

def validate_password(value):
    password = os.environ.get('PASSWORD')
    if not secure_compare(value, password):
        raise ValidationError(
            _('%(value)s is not password'),
            params={'value': value},
        )

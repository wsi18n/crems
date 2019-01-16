'''
custom jwt
custom_jwt.py must be in the directory of django app, or the name of custom jwt file must be "utils.py" 
'''

from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings

def jwt_payload_handler(user):
    """ Custom payload handler
        Token encrpts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        'user_id': user.pk,
        'username': user.username,
        'email': user.email,
        'is_superuser': user.is_superuser,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': timegm(datetime.utcnow().utctimetuple())
    }


def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.
        This function contolls the custom payload afer login or token resfresh. this data is returned through the web API.
    """
    return {
        'token': token,
        'user': {
            'username': user.username,
            'email': user.email,
        }
    }

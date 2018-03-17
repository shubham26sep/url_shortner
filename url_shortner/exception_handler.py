from rest_framework import status
from rest_framework.views import exception_handler

def get_error_message(message):
    # location = None
    while message.__class__ != list:
        # location = list(message)[0]
        message = message[list(message)[0]]
    return message[0]

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None and 'detail' in response.data:
        message = response.data['detail']
        error = {
                    'location': 'server',
                    'message': message
                }
        response.data = {}
        response.data['status'] = response.status_code
        response.data['error'] = error
    else:
        try:
            errors = response.data
            print(errors)
            error_location = list(errors.keys())[0]
            message = errors[error_location]
            message = get_error_message(message)

            response.data = {}
            response.data['status'] = 'FAILED'
            response.data['status_codes'] = ['BAD_DATA']
            response.status_code = status.HTTP_200_OK
        except:
            pass
    return response


def get_custom_error_message(message=None, error_location='server', status=400):
    data = {}
    error = {
                'status': 'FAILED',
                "message":message,
            }
    data['error'] = error
    data['status'] = status

    return data

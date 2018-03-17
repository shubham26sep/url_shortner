from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    response.data = {}
    response.data['status'] = 'FAILED'
    response.data['status_codes'] = ['BAD_DATA']
    response.status_code = status.HTTP_200_OK
    return response

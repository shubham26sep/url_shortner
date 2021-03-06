from rest_framework.response import Response

class SuccessResponse(Response):
    '''
    Custom Response Class to return status and status_codes with data
    '''
    def __init__(self, data=None, status=200):
        result = data
        
        result.update({
            'status': 'OK',
            'status_codes': []
        })

        if status is not None:
            return super().__init__(result, status)
        return super().__init__(result, status)

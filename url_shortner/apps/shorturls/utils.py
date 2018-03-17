from django.core.validators import URLValidator

def validate_url(url):
    '''
    check given url is valid or not
    '''
    validate = URLValidator()
    try:
        validate(url)
    except:
        return False
    return True
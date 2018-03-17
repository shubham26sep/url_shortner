from django.core.validators import URLValidator

def get_base_url(request):
    protocol = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    base_url = '%s://%s' %(protocol, host)
    return base_url


def validate_url(url):
    validate = URLValidator()
    try:
        validate(url)
    except:
        return False
    return True
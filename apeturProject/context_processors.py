from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
        'STATIC_FILE_URL': settings.STATIC_FILE_URL,
        'SITE_FILE_URL': settings.SITE_FILE_URL,
        'USER_FILE_URL': settings.USER_FILE_URL
    }

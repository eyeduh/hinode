from drf_registration.settings import drfr_settings


def get_current_domain(request):

    return drfr_settings.PROJECT_BASE_URL or f'{request.scheme}://{request.get_host()}'
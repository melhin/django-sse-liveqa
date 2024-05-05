from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
async def health(request: HttpRequest, *args, **kwargs):
    return HttpResponse(status=200)

import base64
import functools

from django.http import HttpResponse

from sse_liveqa.settings import BASIC_PASSWORD, BASIC_USER


def view_basicauth(func):

    @functools.wraps(func)
    async def inner(request, realm="Accessing site", *args, **kwargs):
        if "HTTP_AUTHORIZATION" in request.META:
            auth = request.META["HTTP_AUTHORIZATION"].split()
            if len(auth) == 2:
                # NOTE: We are only support basic authentication for now.
                #
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).decode("utf-8").split(":")
                    if uname == BASIC_USER and passwd == BASIC_PASSWORD:
                        return await func(request, *args, **kwargs)

        # Did not provide an authorization header
        # Send a 401 back to them to ask them to authenticate.
        response = HttpResponse()
        response.status_code = 401
        response["WWW-Authenticate"] = 'Basic realm="%s"' % realm
        return response

    return inner

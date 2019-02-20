from django import http
from django.utils.deprecation import MiddlewareMixin


class BookMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("Middleware executed")


class AnotherMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("Another middleware executed")

    def process_response(self, request, response):
        print("AnotherMiddleware process_response executed")
        return response


class UrlPathRecordMiddleware(MiddlewareMixin):
    EXCLUDE_URLS = ['/user/login/', '/user/logout/', '/user/register']

    def process_view(self, request, view_func, *view_args, **view_kwarg):
        if request.path not in UrlPathRecordMiddleware.EXCLUDE_URLS and not request.is_ajax() and request.method == 'GET':
            request.session['url_path'] = request.path


BLOCKED_IPS = []


class BlockedIpMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META['REMOTE_ADDR'] in BLOCKED_IPS:
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')

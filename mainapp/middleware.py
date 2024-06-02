from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class ExceptionHandlingMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        return redirect(reverse('not_found'))

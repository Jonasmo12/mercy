from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticatedUser(view_func):
    """
        Prevents users from accessing certain pages when 
        they are logged in.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
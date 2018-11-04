from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .models import PasswordExpiration


class PasswordExpirationMiddleware(object):
    def process_request(self, request):
        if not isinstance(request.user, AnonymousUser):
            pwd, created = PasswordExpiration.objects.get_or_create(user=request.user)
            if not request.path == reverse('account_change_password'):
                if pwd.expired():
                    return redirect('account_change_password')

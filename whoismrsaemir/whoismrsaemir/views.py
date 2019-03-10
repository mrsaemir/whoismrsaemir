import datetime
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, authentication, permissions
from .serializers import DomainsSerializer
from .models import Domains
from rest_framework.reverse import reverse
import jdatetime


class AdminMixin:
    authentication_classes = (
        authentication.BasicAuthentication,
    )
    permission_classes = (
        permissions.IsAdminUser,
    )


class DomainsViewSet(AdminMixin, viewsets.ModelViewSet):
    queryset = Domains.objects.all()
    serializer_class = DomainsSerializer
    lookup_field = 'url_core'


def update_domain_status(request, url_core):
    try:
        domain = Domains.objects.get(url_core=url_core)
    except ObjectDoesNotExist:
        raise
        raise Http404
    domain.update()
    return HttpResponseRedirect(
        reverse('domain-detail', kwargs={'url_core': domain.url_core}, request=request)
    )



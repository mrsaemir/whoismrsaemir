from rest_framework import viewsets, authentication, permissions
from .serializers import DomainsSerializer
from .models import Domains


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

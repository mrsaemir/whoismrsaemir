from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, authentication, permissions
from .serializers import DomainsSerializer
from .models import Domains, WhoisQueue
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


def run_task(request):
    domain = WhoisQueue.dequeue()
    if domain:
        domain.check_domain()
    return HttpResponse("OK")


def refresh_queue(request):
    from .telegram import send_message
    WhoisQueue.sync()
    # sending response
    send_message(text=f'{str(jdatetime.date.today())}: Queue refreshed successfully.')
    return HttpResponse('OK')


# this function is called everyday and it's job is to check db is synced with queue
def check_queue(request):
    from .telegram import send_message
    jobs = WhoisQueue.objects.count()
    domains = Domains.objects.count()
    if not jobs == domains:
        WhoisQueue.sync()
    send_message(f"{str(jdatetime.date.today())}: Queue Checked")



import datetime
from django.http import HttpResponse
from rest_framework import viewsets, authentication, permissions
from .serializers import DomainsSerializer
from .models import Domains, DailyDomainChecks
from .whois_core import check_domain_status, domain_should_be_deleted_from_daily_checks


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


def daily_check(request):
    today = datetime.date.today()
    domains = DailyDomainChecks.objects.filter(
        url_core__last_check__year__lt=today.year).filter(
        url_core__last_check__month__lt=today.month).filter(
        url_core__last_check__day__lt=today.day)

    # processing today domains
    for domain in domains:
        # domain should be deleted from daily checks because it is registered for another year,
        # if all the postfix status is 'delete'
        status = check_domain_status(domain.url_core.url_core)
        if domain_should_be_deleted_from_daily_checks(status):
            domain.delete()
        else:
            for postfix in status:
                # if it is wait then just leave it until tomorrow.
                if status[postfix] == 'ready':
                    # send an email saying tomorrow is the day.
                    pass
                elif status[postfix] == 'buy':
                    # send an email saying today is the day
                    pass
                else:
                    continue
            # modifying last check(setting it to today).
            domain.save()
    return HttpResponse('OK', status=200)

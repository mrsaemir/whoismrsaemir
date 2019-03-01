import datetime
from django.http import HttpResponseRedirect
from rest_framework import viewsets, authentication, permissions
from .serializers import DomainsSerializer
from .models import Domains, DailyDomainChecks
from .whois_core import check_domain_status, domain_should_be_deleted_from_daily_checks,\
    judge_status_based_on_days, domain_should_be_added_to_daily_checks
from rest_framework.reverse import reverse


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
        status, count_down = check_domain_status(domain.url_core.url_core)
        if domain_should_be_deleted_from_daily_checks(status):
            domain.delete()
        else:
            for postfix, action in status.item():
                # if it is wait then just leave it until tomorrow.
                if action == 'ready':
                    # send an email saying tomorrow is the day.
                    pass
                elif action == 'buy':
                    # send an email saying today is the day
                    pass
            # modifying last check(setting it to today).
            domain.save()
    return HttpResponseRedirect(reverse('domain-list'))


def weekly_check(request):
    domains = Domains.objects.all()
    for domain in domains:
        # updating info on domain model
        count_down = domain.get_count_down_status()
        res = judge_status_based_on_days(count_down)
        if domain_should_be_added_to_daily_checks(res):
            domain.add_to_daily_checks()
        for postfix, action in res.items():
            if action == 'ready':
                # send an email and say tomorrow is the day.
                pass
            elif action == 'buy':
                # send an email and say today is the day.
                pass
    return HttpResponseRedirect(reverse('domain-list'))

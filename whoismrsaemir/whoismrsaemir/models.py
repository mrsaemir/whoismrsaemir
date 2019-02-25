import datetime
from django.db import models
import jdatetime
from jsonfield import JSONField
from .whois_core import check_domain_status


# this list is checked every week.
class Domains(models.Model):
    added_dt = models.DateTimeField(auto_now_add=True)
    last_check = models.DateField(auto_now=True)
    url_core = models.CharField(max_length=250, unique=True)
    count_down_status = JSONField(null=True)

    def __str__(self):
        dt = jdatetime.GregorianToJalali(gyear=self.added_dt.year,
                                         gmonth=self.added_dt.month,
                                         gday=self.added_dt.day)
        return "{}/{}/{}".format(dt.jyear, dt.jmonth, dt.jday)

    def get_count_down_status(self):
        today = datetime.date.today()
        # if no count_down in obj instance
        if not self.count_down_status:
            status, count_down = check_domain_status(self.url_core)
            self.count_down_status = count_down
            self.save()
            return count_down
        # updating existing status
        if today != self.last_check:
            status, count_down = check_domain_status(self.url_core)
            self.count_down_status = count_down
            self.save()
        else:
            count_down = self.count_down_status
        return count_down

    def add_to_daily_checks(self):
        if not DailyDomainChecks.objects.filter(url_core=self):
            obj = DailyDomainChecks()
            obj.url_core = self
            obj.save()
            return obj
        return None


# this list is checked every day.
# for urls with higher possibility (urls with expiration with less than 30 days)
class DailyDomainChecks(models.Model):
    added_dt = models.DateTimeField(auto_now_add=True)
    url_core = models.OneToOneField(Domains, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        dt = jdatetime.GregorianToJalali(gyear=self.added_dt.year,
                                         gmonth=self.added_dt.month,
                                         gday=self.added_dt.day)
        return "{}/{}/{}".format(dt.jyear, dt.jmonth, dt.jday)

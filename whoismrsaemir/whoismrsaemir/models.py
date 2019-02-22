from django.db import models
import jdatetime


# this list is checked every week.
class Domains(models.Model):
    added_dt = models.DateTimeField(auto_now_add=True)
    last_check = models.DateTimeField(auto_now=True)
    url_core = models.CharField(max_length=250, unique=True)

    def __str__(self):
        dt = jdatetime.GregorianToJalali(gyear=self.added_dt.year,
                                         gmonth=self.added_dt.month,
                                         gday=self.added_dt.day)
        return "{}/{}/{}".format(dt.jyear, dt.jmonth, dt.jday)


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

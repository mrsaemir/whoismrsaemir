from django.db import models


# this list is checked every week.
class Domains(models.Model):
    added_dt = models.DateTimeField(auto_now_add=True)
    url_core = models.CharField(max_length=250, unique=True)


# this list is checked every day.
# for urls with higher possibility (urls with expiration with less than 30 days)
class DailyDomainChecks(models.Model):
    added_dt = models.DateTimeField(auto_now_add=True)
    url_core = models.ForeignKey(Domains, on_delete=models.CASCADE)

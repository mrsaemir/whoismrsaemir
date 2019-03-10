import datetime
from django.db import models
import jdatetime
from jsonfield import JSONField
from .whois_core import check_domain_status
from .telegram import send_message as t_message


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

    def update(self):
        status, count_down = check_domain_status(self.url_core)
        self.count_down_status = count_down
        self.save()
        return status, count_down

    def get_count_down_status(self):
        # if no count_down in obj instance
        if not self.count_down_status:
            status, count_down = self.update()
            return count_down

        # updating existing status
        if not self.is_checked_today():
            status, count_down = self.update()
        else:
            count_down = self.count_down_status
        return count_down

    def is_checked_today(self):
        today = datetime.date.today()
        if self.last_check == today:
            return True
        return False

    # notifying in telegram if domain is about to expire
    def notify_about_expiration(self, chat_id, postfix):
        # postfix is the available domain's postfix. exp: ir, com, org
        text = f"Domain {self.url_core}.{postfix} is about to expire."
        t_message(chat_id=chat_id, text=text)

    def notify_expired(self, chat_id, postfix):
        text = f"Domain {self.url_core}.{postfix} is expired."
        t_message(chat_id=chat_id, text=text)

    def notify_problem_detecting_expiration(self, chat_id, postfix):
        text = f"There was a problem detecting expiration date on {self.url_core}.{postfix}."
        t_message(chat_id=chat_id, text=text)

    def add_to_queue(self):
        if not WhoisQueue.objects.filter(domain=self):
            queue = WhoisQueue()
            queue.domain = self
            queue.save()

    def save(self, *args, **kwargs):
        super(Domains, self).save(*args, **kwargs)
        self.add_to_queue()


# a simple queue for handling whois jobs
class WhoisQueue(models.Model):
    domain = models.ForeignKey(Domains, on_delete=models.CASCADE)

    @staticmethod
    def dequeue():
        # adding the item, then deleting the first queue item
        first = WhoisQueue.objects.first()
        if first:
            last = WhoisQueue()
            last.domain = first
            last.save()
            return first.domain
        else:
            return None

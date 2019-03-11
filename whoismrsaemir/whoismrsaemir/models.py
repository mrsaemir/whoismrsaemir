import datetime
from django.db import models
import jdatetime
from jsonfield import JSONField
from .whois_core import (check_domain_status, judge_status_based_on_days, domain_should_be_deleted_from_daily_checks)
from .telegram import send_message as t_message
from django.conf import settings


# this list is checked every week.
class Domains(models.Model):
    added_dt = models.DateTimeField(auto_now_add=True)
    last_check = models.DateField(auto_now=True)
    next_check = models.DateField(null=True)
    url_core = models.CharField(max_length=250, unique=True)
    count_down_status = JSONField(null=True)

    def __str__(self):
        dt = jdatetime.GregorianToJalali(gyear=self.added_dt.year,
                                         gmonth=self.added_dt.month,
                                         gday=self.added_dt.day)
        return "{} - {}/{}/{}".format(self.url_core, dt.jyear, dt.jmonth, dt.jday)

    def update(self):
        status, count_down = check_domain_status(self.url_core)
        self.count_down_status = count_down
        self.save()
        return status, count_down

    def get_count_down_status(self):
        # if no count_down in obj instance
        if not self.count_down_status:
            status, count_down = self.update()
            return status, count_down

        # updating existing status
        if not self.is_checked_today():
            status, count_down = self.update()
        else:
            count_down = self.count_down_status
            status = judge_status_based_on_days(count_down)
        return status, count_down

    def is_checked_today(self):
        today = datetime.date.today()
        # if a next check is set then check if we have reached the date of the next check or passed it.
        # in this condition we should check again, else we should ignore checking.
        if self.next_check:
            if self.next_check > today:
                return True

        # if it should be checked in the next 30 days this function returns True
        # never checked before
        if not self.count_down_status:
            return False
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

    def check_domain(self):
        # process domain if it is not checked today.
        if not self.is_checked_today():
            status, count_down = self.get_count_down_status()
            # nothing is even about expiration
            if domain_should_be_deleted_from_daily_checks(status):
                # set next check flag
                self.next_check = datetime.date.today() + datetime.timedelta(days=30)
                self.save()
                return
            for postfix, action in status.items():
                if action == "ready":
                    self.next_check = None
                    self.save()
                    self.notify_about_expiration(chat_id=settings.OWNER_TELEGRAM_USERNAME,
                                                 postfix=postfix)
                elif action == "buy":
                    self.next_check = None
                    self.save()
                    self.notify_expired(chat_id=settings.OWNER_TELEGRAM_USERNAME,
                                        postfix=postfix)
                elif action == "no-info":
                    self.next_check = None
                    self.save()
                    self.notify_problem_detecting_expiration(chat_id=settings.OWNER_TELEGRAM_USERNAME,
                                                             postfix=postfix)
                elif action == "waiting":
                    self.next_check = None
                    self.save()

    def save(self, *args, **kwargs):
        super(Domains, self).save(*args, **kwargs)
        self.add_to_queue()


# a simple queue for handling whois jobs
class WhoisQueue(models.Model):
    domain = models.ForeignKey(Domains, on_delete=models.CASCADE)
    added = models.DateTimeField(primary_key=True, auto_now=True)

    def save(self, *args, **kwargs):
        super(WhoisQueue, self).save(*args, **kwargs)

    @staticmethod
    def dequeue():
        # adding the item, then deleting the first queue item
        first = WhoisQueue.objects.first()
        if first:
            last = WhoisQueue()
            last.domain = first.domain
            last.save()
            first.delete()
            return first.domain
        else:
            return None

    @staticmethod
    def sync():
        # deleting all items of the queue
        domains = WhoisQueue.objects.all()
        for domain in domains:
            domain.delete()
        # adding all items to queue
        domains = Domains.objects.all()
        for domain in domains:
            domain.add_to_queue()

import re
import bs4 as bs
import urllib.request
import datetime
import threading
supported_postfixes = ['ir', 'com', 'org']


# note : the class behaviour on unsupported domains may be unpredictable and may be not true.
# currently, fully supported domains are: .com and .ir
# this function returns -1 if there is no information.
class WhoIsMrSaemir(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url.lower()
        if self.url.count('.') != 1:
            raise ValueError("Non standard url, Enter your url like the example: 'gitlab.com'")
        self.expiration = None
        self.core, self.postfix = self.url.split('.')

    def is_ir(self):
        return bool(re.search(r'.ir', self.url))

    def get_expiration(self):
        if self.expiration:
            return self.expiration

        sauce = urllib.request.urlopen('https://who.is/whois/%s' % self.url)
        soup = bs.BeautifulSoup(sauce, 'lxml')
        if self.url.split('.')[1] == 'ir':
            ex = 'expire-date:'
            dp = 1
        else:
            ex = 'Expires'
            dp = 2
        list = soup.text.split()
        i = 0
        j = 0
        for s in list:
            if s == ex:
                j = i
                break
            i += 1
        try:
            dt = datetime.datetime.strptime(list[j + dp], '%Y-%m-%d')
            self.expiration = dt
            return dt
        except:
            return None

    def can_buy(self):
        expiration = self.get_expiration()
        if not expiration:
            return -1
        if expiration <= datetime.datetime.now():
            return True
        return False

    def days_till_expiration(self):
        expiration = self.get_expiration()
        if not expiration:
            return -1
        return (expiration - datetime.datetime.now()).days

    def run(self):
        return self.get_expiration()


# a function that checks if any of the domains
# requested in the list are available to buy, should be deleted from daily query
# or should wait on them. it also returns count down number to expiration date.
def check_domain_status(url_core):
    expiration_count_down = {}
    global supported_postfixes
    threads = []
    for postfix in supported_postfixes:
        threads.append(WhoIsMrSaemir(url=url_core + '.' + postfix))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    for thread in threads:
        days = thread.days_till_expiration()
        expiration_count_down[thread.postfix] = days
    status = judge_status_based_on_days(expiration_count_down)
    return status, expiration_count_down


def judge_status_based_on_days(count_down_status):
    status = {}
    for postfix, days in count_down_status.items():
        if days > 30:
            # they have purchased for another year, shit!
            status[postfix] = 'delete'
        elif 2 <= days <= 30:
            status[postfix] = 'wait'
        elif days == 1:
            status[postfix] = 'ready'
        elif days == -1:
            status[postfix] = 'no-info'
        else:
            status[postfix] = 'buy'
    return status


def domain_should_be_deleted_from_daily_checks(status):
    for postfix, action in status.items():
        if action != 'delete':
            return False
    return True

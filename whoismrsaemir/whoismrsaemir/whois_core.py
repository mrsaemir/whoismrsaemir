import re
import bs4 as bs
import urllib.request
import datetime

supported_postfixes = ['ir', 'com', 'net', 'info', 'org']


# note : the class behaviour on unsupported domains may be unpredictable and may be not true.
# currently, fully supported domains are: .com and .ir
class WhoIsMrSaemir:
    def __init__(self, url):
        self.url = url.lower()
        if self.url.count('.') != 1:
            raise ValueError("Non standard url, Enter your url like the example: 'gitlab.com'")

    def _ir_whois_expiration(self):
        sauce = urllib.request.urlopen('https://who.is/whois/%s' % self.url)
        soup = bs.BeautifulSoup(sauce, 'lxml')
        texts = soup.text.split()
        i = 0
        j = 0
        for s in texts:
            if s == 'expire-date:':
                j = i
                break
            i += 1
        try:
            dt = datetime.datetime.strptime(texts[j + 1], '%Y-%m-%d')
            return dt
        except:
            return None

    def _non_ir_whois_expiration(self):
        from whois import whois
        try:
            query = whois(url=self.url)
            return query.expiration_date
        except:
            return None

    def is_ir(self):
        return bool(re.search(r'.ir', self.url))

    def get_expiration(self):
        if self.is_ir():
            return self._ir_whois_expiration()
        else:
            expiration = self._non_ir_whois_expiration()
            if isinstance(expiration, list):
                return expiration[0]
            else:
                return expiration

    def can_buy(self):
        expiration = self.get_expiration()
        if not expiration:
            return True
        if expiration <= datetime.datetime.now():
            return True
        return False

    def days_till_expiration(self):
        expiration = self.get_expiration()
        if not expiration:
            return 0
        return (expiration - datetime.datetime.now()).days


# a function that checks if any of the domains
# requested in the list are available to buy, should be deleted from daily query
# or should wait on them. it also returns count down number to expiration date.
def check_domain_status(url_core):
    expiration_count_down = {}
    global supported_postfixes
    for postfix in supported_postfixes:
        whois = WhoIsMrSaemir(url=url_core + '.' + postfix)
        days = whois.days_till_expiration()
        expiration_count_down[postfix] = days
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
        else:
            status[postfix] = 'buy'
    return status


def domain_should_be_deleted_from_daily_checks(status):
    delete = True
    for postfix in status:
        if status[postfix] != 'delete':
            delete = False
            return delete
    return delete

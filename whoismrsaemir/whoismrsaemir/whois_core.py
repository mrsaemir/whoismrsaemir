import re
import bs4 as bs
import urllib.request
import datetime


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
# requested in the list are available to buy, should be deleted from dailt query
# or should wait on them
def check_domain_status(url_core):
    result = {}
    supported_postfixes = ['ir', 'com', 'net']
    for postfix in supported_postfixes:
        whois = WhoIsMrSaemir(url=url_core + '.' + postfix)
        days = whois.days_till_expiration()
        if days > 30:
            # they have purchased for another year, shit!
            result[postfix] = 'delete'
        elif 2 <= days <= 30:
            result[postfix] = 'wait'
        elif days == 1:
            result[postfix] = 'ready'
        else:
            result[postfix] = 'buy'
    return result


def domain_should_be_deleted_from_daily_checks(status):
    delete = True
    for postfix in status:
        if status[postfix] != 'delete':
            delete = False
            return delete
    return delete

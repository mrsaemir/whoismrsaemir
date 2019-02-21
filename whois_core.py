import bs4 as bs
import urllib.request
import datetime


class WhoIsMrSaemir:
    def __init__(self, url):
        self.url = url

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
        import re
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

from rest_framework import serializers
from rest_framework.reverse import reverse
import jdatetime
from .models import Domains
import datetime


class DomainsSerializer(serializers.ModelSerializer):
    added_on = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    expiration_count_down = serializers.SerializerMethodField()
    last_check = serializers.SerializerMethodField()
    next_check = serializers.SerializerMethodField()

    class Meta:
        model = Domains
        fields = ('url_core', 'added_on', 'last_check', 'next_check', 'expiration_count_down',
                  'links')
        extra_kwargs = {
            'url': {'lookup_field': 'url_core'}
        }

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('domain-detail', kwargs={'url_core': obj.url_core}, request=request),
            'update': reverse('update-detail', kwargs={'url_core': obj.url_core}, request=request),
        }

    @staticmethod
    def get_added_on(obj):
        dt = obj.added_dt
        dt = jdatetime.GregorianToJalali(gyear=dt.year, gmonth=dt.month, gday=dt.day)
        return "{}/{}/{}".format(dt.jyear, dt.jmonth, dt.jday)

    @staticmethod
    def get_expiration_count_down(obj):
        return obj.count_down_status

    @staticmethod
    def get_last_check(obj):
        if not obj.count_down_status:
            return "Not Checked."
        dt = obj.last_check
        dt = jdatetime.GregorianToJalali(gyear=dt.year, gmonth=dt.month, gday=dt.day)
        res = "{}/{}/{}".format(dt.jyear, dt.jmonth, dt.jday)
        if obj.last_check == datetime.date.today():
            res += "(today)"
        return res

    @staticmethod
    def get_next_check(obj):
        if not obj.next_check:
            return "NOW"
        dt = obj.next_check
        dt = jdatetime.GregorianToJalali(gyear=dt.year, gmonth=dt.month, gday=dt.day)
        res = "{}/{}/{}".format(dt.jyear, dt.jmonth, dt.jday)
        return res


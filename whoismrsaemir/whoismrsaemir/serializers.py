from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Domains


class DomainsSerializer(serializers.ModelSerializer):
    added_on = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Domains
        fields = ('url_core', 'added_on', 'links')
        lookup_field = 'url_core'
        extra_kwargs = {
            'url': {'lookup_field': 'url_core'}
        }

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('domain-detail', kwargs={'url_core': obj.url_core}, request=request)
        }

    def get_added_on(self, obj):
        import jdatetime
        dt = obj.added_dt
        dt = jdatetime.GregorianToJalali(gyear=dt.year, gmonth=dt.month, gday=dt.day)
        return "{}/{}/{}".format(dt.jyear, dt.jmonth, dt.jday)

import uuid
from rest_framework import serializers

from url_shortner.apps.shorturls.models import Url
from url_shortner.apps.shorturls import utils

class FetchShortUrlSerializer(serializers.ModelSerializer):
    long_url = serializers.CharField()

    class Meta:
        model = Url
        fields = ('long_url',)

    def create(self, validated_data):
        request = self.context.get('request')
        long_url = validated_data['long_url']
        
        instance = Url.objects.filter(long_url=long_url).first()
        if instance:
            return instance

        short_url_created = False

        while not short_url_created:
            hashcode = str(uuid.uuid4())[:8]
            base_url = utils.get_base_url(request)
            short_url = '%s/%s/' % (base_url, hashcode)
            
            if not Url.objects.filter(short_url=short_url).exists():
                short_url_created = True
                break

        instance = Url.objects.create(long_url=long_url, short_url=short_url)

        return instance


class FetchMultipleShortUrlSerializer(serializers.Serializer):
    long_urls = serializers.ListField(child=serializers.CharField())


class FetchLongUrlSerializer(serializers.Serializer):

    short_url = serializers.CharField()

    # def validate(self, attrs):
    #     short_url = attrs['short_url']

    #     url = Url.objects.filter(short_url=short_url).first()
    #     if not url:
    #         raise serializers.ValidationError('SHORT_URLS_NOT_FOUND')

    #     self.url = url
    #     return attrs
        

class FetchMultipleLongUrlSerializer(serializers.Serializer):
    short_urls = serializers.ListField(child=serializers.CharField())
    
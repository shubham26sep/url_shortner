import uuid
from rest_framework.reverse import reverse
from rest_framework import serializers

from url_shortner.apps.shorturls.models import Url

class FetchShortUrlSerializer(serializers.ModelSerializer):
    long_url = serializers.CharField()

    class Meta:
        model = Url
        fields = ('long_url',)

    def create(self, validated_data):
        request = self.context.get('request')
        long_url = validated_data['long_url']
        
        # Return instance if long url already exists in database
        instance = Url.objects.filter(long_url=long_url).first()
        if instance:
            return instance


        short_url_created = False

        # creating hashcode for long url
        while not short_url_created:
            hashcode = str(uuid.uuid4())[:8]
            short_url = request.build_absolute_uri(reverse('short-url-server', args=[hashcode]))
            
            if not Url.objects.filter(short_url=short_url).exists():
                short_url_created = True
                break

        # creating url object in database
        instance = Url.objects.create(long_url=long_url, short_url=short_url)

        return instance


class FetchMultipleShortUrlSerializer(serializers.Serializer):
    long_urls = serializers.ListField(child=serializers.CharField())


class FetchLongUrlSerializer(serializers.Serializer):

    short_url = serializers.CharField()
            

class FetchMultipleLongUrlSerializer(serializers.Serializer):
    short_urls = serializers.ListField(child=serializers.CharField())
    
from rest_framework import views
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponseRedirect

from url_shortner.apps.shorturls.models import Url
from url_shortner.apps.shorturls.serializers import (FetchShortUrlSerializer, FetchLongUrlSerializer,
    FetchMultipleShortUrlSerializer, FetchMultipleLongUrlSerializer)

from url_shortner.apps.shorturls import utils
from url_shortner.response import SuccessResponse


class FetchShortUrlView(views.APIView):
    '''
    API to fetch short url from long url
    '''

    serializer_class = FetchShortUrlSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        long_url = serializer.validated_data['long_url']

        if not utils.validate_url(long_url):
            return Response({'status': 'FAILED', 'status_codes': ['INVALID_URLS']})

        # get or create short url for long url
        url = serializer.save()
        short_url = url.short_url
        return SuccessResponse({'short_url': short_url})


class FetchMultipleShortUrlsView(views.APIView):
    '''
    API to fetch multiple short urls from list of long urls
    '''

    serializer_class = FetchMultipleShortUrlSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        long_urls = serializer.validated_data['long_urls']

        # validating list of long_urls
        invalid_urls = []
        for url in long_urls:
            if not utils.validate_url(url):
                invalid_urls.append(url)

        if invalid_urls:
            return Response({'invalid_urls':invalid_urls, 'status': 'FAILED', 'status_codes': ['INVALID_URLS']})

        long_urls_data = [{'long_url': long_url} for long_url in long_urls]
        
        # get or create short url for each long url
        serializer = FetchShortUrlSerializer(data=long_urls_data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()

        # returning short urls data for each long url
        short_urls = {}
        for instance in instances:
            short_urls.update({instance.long_url: instance.short_url})

        return SuccessResponse({'short_urls': short_urls, 'invalid_urls': invalid_urls})


class FetchLongUrlView(views.APIView):
    '''
    API to fetch short url from long url
    '''

    serializer_class = FetchLongUrlSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_url = serializer.validated_data['short_url']

        
        # validating url and checking if url exists in database
        if not utils.validate_url(short_url) or not Url.objects.filter(short_url=short_url).first():
            return Response({'status': 'FAILED', 'status_codes': ['SHORT_URLS_NOT_FOUND']})

        # returning short_url respective long_url
        url = Url.objects.filter(short_url=short_url).first()
        return SuccessResponse({'long_url': url.long_url})


class FetchMultipleLongUrlsView(views.APIView):
    '''
    API to fetch multiple long urls from list of short urls
    '''

    serializer_class = FetchMultipleLongUrlSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_urls = serializer.validated_data['short_urls']
        
        # validating list of short_urls
        invalid_urls = []
        for url in short_urls:
            if not utils.validate_url(url):
                invalid_urls.append(url)

        if invalid_urls:
            return Response({'invalid_urls': invalid_urls, 'status': 'FAILED', 'status_codes': ['INVALID_URLS']})

        instances = []

        # finding all short urls instances from database
        for short_url in short_urls:
            instance = Url.objects.filter(short_url=short_url).first()
            if not instance:
                error = {'invalid_urls': [short_url], 'status': 'FAILED', "status_codes": ["SHORT_URLS_NOT_FOUND"]}
                return Response(error)

            instances.append(instance)

        # returning long urls data for each short url
        long_urls = {}
        for instance in instances:
            long_urls.update({instance.short_url: instance.long_url})

        return SuccessResponse({'long_urls': long_urls, 'invalid_urls': invalid_urls})


class ShortUrlServerView(views.APIView):
    '''
    API to redirect to actual url from short url
    '''
    def post(self, request, hashcode):
        short_url = request.build_absolute_uri(reverse('short-url-server', args=[hashcode]))
        # validating url and checking if url exists in database
        if not utils.validate_url(short_url) or not Url.objects.filter(short_url=short_url).first():
            return Response({'status': 'FAILED', 'status_codes': ['SHORT_URLS_NOT_FOUND']})

        url = Url.objects.filter(short_url=short_url).first()
        if not url:
            error = {'invalid_urls': [short_url], 'status': 'FAILED', "status_codes": ["SHORT_URLS_NOT_FOUND"]}
            return Response(error)

        # Increase url access count
        url.access_count = url.access_count+1
        url.save()

        long_url = url.long_url
        # redirecting short url to long url
        return HttpResponseRedirect(redirect_to=long_url)


class FetchShortUrlAccessCount(views.APIView):
    '''
    API to fetch the number of times as short URL was used to access the long URL
    '''

    serializer_class = FetchLongUrlSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_url = serializer.validated_data['short_url']

        # validating url and checking if url exists in database
        if not utils.validate_url(short_url) or not Url.objects.filter(short_url=short_url).first():
            return Response({'status': 'FAILED', 'status_codes': []})

        # fetch access count for given short url from database
        url = Url.objects.filter(short_url=short_url).first()
        access_count = url.access_count
        return SuccessResponse({'count': access_count})


class CleanUrlView(views.APIView):
    '''
    API to clean urls from database
    '''
    def post(self, request):
        # deleting all urls from database
        Url.objects.all().delete()
        return SuccessResponse({})

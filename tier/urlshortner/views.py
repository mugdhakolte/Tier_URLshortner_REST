import random
import string

from django.shortcuts import redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from urlshortner.models import *
from urlshortner.serializers import *


class ShortURL(APIView):

    def post(self, request):
        serializer = TierURLSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        request_url = serializer.data['main_url']
        # base_url = 'tier.app'
        base_url = '127.0.0.1:8001'
        random_string = ''.join(random.choices(string.ascii_uppercase +
                                               string.digits + string.ascii_lowercase,
                                               k=10))
        short_url = "http://{}/{}/".format(base_url, random_string)
        validate = URLValidator()

        try:
            validate(short_url)
        except ValidationError as e:
            print(e)

        try:
            obj = TierURL.objects.get(short_url=short_url)
        except TierURL.DoesNotExist:
            obj = TierURL(main_url=request_url, short_url=short_url)
            obj.save()
        data = {
            'new_url': obj.short_url,
            'main_url': request_url,
            'random_string': random_string
        }
        return Response(data, status=status.HTTP_200_OK)


class VisitURL(APIView):

    def get(self, request, url):
        # request_url = 'http://tier.app/{}/'.format(url)
        request_url = 'http://127.0.0.1:8001/{}/'.format(url)

        try:
            obj = TierURL.objects.get(short_url=request_url)
            try:
                visit_obj = URLVisit.objects.get(tier_url=obj)
                visit_obj.visits += 1
                visit_obj.save()
                return redirect(visit_obj.tier_url.main_url)

            except URLVisit.DoesNotExist:
                visit_obj = URLVisit(tier_url=obj, visits=1)
                visit_obj.save()
                return redirect(visit_obj.tier_url.main_url)
        except TierURL.DoesNotExist:
            return redirect('shorten_url')


class VisitedURLCount(APIView):

    def get(self, request, random_string):
        # base_url = 'tier.app'
        base_url = '127.0.0.1:8001'
        short_url = "http://{}/{}/".format(base_url, random_string)
        try:
            obj = TierURL.objects.get(short_url=short_url)
            try:
                visit_obj = URLVisit.objects.get(tier_url=obj)
                data = {
                    'visits': visit_obj.visits,
                    'short_url': visit_obj.tier_url.short_url
                }
                return Response(data, status=status.HTTP_200_OK)

            except URLVisit.DoesNotExist:
                data = {
                    'short_url': obj.short_url,
                    'no_visits': True
                }
                return Response(data, status=status.HTTP_200_OK)
        except TierURL.DoesNotExist:
            pass
        data = {}
        return Response(data, status=status.HTTP_200_OK)


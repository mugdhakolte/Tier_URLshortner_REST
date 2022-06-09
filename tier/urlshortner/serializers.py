from rest_framework.serializers import ModelSerializer
from urlshortner.models import *


class TierURLSerializer(ModelSerializer):
    class Meta:
        model = TierURL
        fields = ['main_url']

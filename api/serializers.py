from rest_framework import serializers
from receiver.models import Endpoint, APICall

class EndpointSerializer(serializers.ModelSerializer):
    response_image = serializers.ImageField(required=False, allow_null=True, use_url=True)
    class Meta:
        model = Endpoint
        fields = '__all__'

class APICallSerializer(serializers.ModelSerializer):
    class Meta:
        model = APICall
        fields = '__all__'
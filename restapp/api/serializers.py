from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from restapp.models import PostCardIDEvent



class restappSerializer(ModelSerializer):
    f_evento = serializers.DateField(format='%Y-%m-%d') 
    h_evento = serializers.TimeField(format='%H:%M:%S') 
    class Meta:
        model = PostCardIDEvent
        fields = ['id', 'deviceID','cardID', 'f_evento', 'h_evento', 'evento']
        
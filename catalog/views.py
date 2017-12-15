from django.shortcuts import render
from rest_framework import serializers
from datetime import datetime
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

# Create your views here.
class JSONResponse(HttpResponse): #An HttpResponse that renders its content into JSON.
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class XYZSerializer(serializers.Serializer): # define a serializer with a datetime
    hora_actual = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

def timenow(request):
    x = XYZSerializer(data={'hora_actual':datetime.now()})
    x.is_valid()
    return JSONResponse(x.data)

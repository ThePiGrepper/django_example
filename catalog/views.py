from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from rest_framework import serializers,status
from rest_framework.renderers import JSONRenderer

from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .models import User
from .serializers import UserSerializer

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

class UserList(APIView): #List users or add new one
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView): #Read, update, delete user data
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        user = UserSerializer(user)
        return Response(user.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)

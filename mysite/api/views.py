from api.serializers import UserSerializer
from api.serializers import MilkSerializer
from gamification.models import Milk
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework import status
from django.http import Http404

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view  
from django.contrib.auth.models import User

from rest_framework import mixins
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here
    
    def get(self, request):
        print(request.user)
        content = {'message': request.user.id}
        return Response(content)


class getUserIdView(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here
    
    def get(self, request):
        print(request.user)
        content = {'message': request.user.id}
        return Response(content)



class MilkList(generics.ListCreateAPIView):
    queryset = Milk.objects.all().order_by('-id')
    serializer_class = MilkSerializer




class MilkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Milk.objects.all().order_by('-id')
    serializer_class = MilkSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# @api_view(['GET', 'POST'])
# def milk_list(request):
    
#     if request.method == 'GET':
#         milks = Milk.objects.all().order_by('-id')
#         serializer = MilkSerializer(milks, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         print(request.data)
#         data = JSONParser().parse(request)
#         serializer = MilkSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400) 
        


# @api_view(['GET', 'PUT', 'DELETE'])
# def milk_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         milk = Milk.objects.get(pk=pk)
#     except Milk.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = MilkSerializer(milk)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = MilkSerializer(milk, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         milk.delete()
#         return HttpResponse(status=204)


    
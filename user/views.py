
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework import generics, serializers
from user.serializers import RegisterSerializer,MyTokenObtainPairSerializer,ProductSerializer,ProductCreateSerializer
from rest_framework.response import Response
from user.models import Product, User
from rest_framework import status
from django.http import Http404
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    # permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class=ProductCreateSerializer
    
    def list(self, request):
        queryset = Product.objects.all()
        name=request.GET.get('name')
        sort=request.GET.get('sort')
        if sort:
            queryset=Product.objects.filter(name__icontains=sort).order_by('-id')

        if name:
            queryset=Product.objects.filter(name__icontains=name)
        else:
            queryset=queryset
        page = self.paginate_queryset(queryset)
        serializer = ProductSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    

    def create(self, request, format=None):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    

class ProductDetailView(APIView):
    serializer_class=ProductCreateSerializer
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):

        queryset = self.get_object(pk)
        serializer = ProductSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = ProductCreateSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
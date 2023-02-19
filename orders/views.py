from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.response import Response
from .import serializers
from .models import Order
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from authentication.models import User
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
    
User = get_user_model()

class OrderCreateListView(generics.GenericAPIView):
    serializer_class = serializers.OrderCreationSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(operation_summary="List All Orders")
    def get(self,request):
       orders = Order.objects.all()
       serializer = self.serializer_class(instance=orders,many=True)
       return Response(data=serializer.data,status=status.HTTP_200_OK)
        
    @swagger_auto_schema(operation_summary="Update Order Details")
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        user=request.user
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class OrderDetailsView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(operation_summary="Retrieve order details")
    def get(self,request,order_id):
        order = get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary="Update order detail")
    def put(self,request,order_id):
        data = request.data
        order = get_object_or_404(Order, pk=order_id)
        serializer = self.serializer_class(data=data,instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_summary="Delete Order")
    def delete(self,request,order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UpdateOrderStatus(generics.GenericAPIView):
    serializer_class=serializers.OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]
    
    @swagger_auto_schema(operation_summary="Update Order Status")
    def put(self, request, order_id):
        data=request.data
        order = get_object_or_404(Order, pk=order_id)
        serializer=self.serializer_class(data=data,instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)            
        
class UserOrdersView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    
    @swagger_auto_schema(operation_summary="Retrieve user Orders")
    def get(self,request,user_id):
        user=User.objects.get(pk=user_id)
        orders = Order.objects.all().filter(customer=user)
        serializer = self.serializer_class(instance=orders,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class UserOrderDetail(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    
    @swagger_auto_schema(operation_summary="List user order details")
    def get(self,request,user_id,order_id):
        user=User.objects.get(pk=user_id)
        order=Order.objects.all().filter(customer=user).get(pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
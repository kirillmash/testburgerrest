from django.http import Http404, JsonResponse

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dish, Order, DishesInOrder
from .serializers import MenuSerializer, OrderSerializer, PriceSerializer


class MenuViews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dishes = Dish.objects.filter(in_menu=True)
        serializer = MenuSerializer(dishes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            raise ParseError(detail=serializer.errors)
        o = Order()
        o.restaurant = serializer.validated_data['restaurant']
        o.operator_id = request.user.id
        o.save()
        dishes = []
        for dish in serializer.validated_data['dishes']:
            DishesInOrder.objects.create(order_id=o.id, dish=dish['dish'], quantity=dish.get('quantity', 1))
            dishes.append({'dish': dish['dish'].name, 'quantity': dish.get('quantity', 1), 'price': dish['dish'].price})
        total = 0
        for dish in DishesInOrder.objects.filter(order=o.id):
            total += dish.total_price
        o.total_price = total
        o.save()
        data = {
            'order_id': o.id,
            'restaurant': o.restaurant.name,
            'operator': f"{o.operator.first_name} {o.operator.last_name}",
            'total_price': o.total_price,
            'dishes': dishes,
            'created_at': o.created_at

        }
        return JsonResponse(data, status=status.HTTP_200_OK)


class ChangePriceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get_object(pk):
        try:
            return Dish.objects.get(pk=pk)
        except Dish.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        dish = self.get_object(pk)
        serializer = PriceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        dish.price = serializer.data['price']
        dish.save()
        return Response(MenuSerializer(dish).data, status=status.HTTP_200_OK)

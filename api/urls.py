from django.urls import path
from .views import MenuViews, OrderViews, ChangePriceView
from rest_framework.authtoken import views

urlpatterns = [
    path('menu/', MenuViews.as_view()),
    path('order/', OrderViews.as_view()),
    path('auth_token/', views.obtain_auth_token),
    path('change_price/<int:pk>/', ChangePriceView.as_view())

]

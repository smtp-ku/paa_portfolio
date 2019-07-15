from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_ticker_description, name='index'),
    path('code/', views.get_code_all, name="code"),
    path('ticker/', views.get_ticker_all, name="ticker"),
    path('ticker/<str:code>/', views.get_ticker, name='ticker')
]
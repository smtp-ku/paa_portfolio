from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'ticker'

ticker_list = views.TickerView.as_view({
    'post': 'create',
    'get':'list'
})

ticker_detail = views.TickerView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('', ticker_list, name='ticker_list'),
    path('<int:pk>/', ticker_detail, name='ticker_detail'),
])


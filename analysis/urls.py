from django.urls import path

from . import views
from . import I_basic

urlpatterns = [
    path('', views.index, name='index'),
    path('basic/', I_basic.basic, name='basic'),
    path('search/', I_basic.search, name='search'),
    path('macd/', views.macd, name='macd'),
    path('kdj/', views.kdj, name='kdj'),
]
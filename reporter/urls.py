from django.urls import path
from . import views

app_name = 'reporter'
urlpatterns = [
    path('', views.index, name='index'),
    path('api_report', views.api_report, name='api_report'),
    path('bulk_report', views.bulk_report, name='bulk_report'),
    path('kannel_report', views.kannel_report, name='kannel_report'),


]
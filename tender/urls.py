from django.urls import path, include
from . import views

urlpatterns = [
    path('ping/', views.PingView.as_view()),
    #path('tenders/'),
    path('tenders/new/', views.TenderNewView.as_view()),
    #path('tenders/my/'), # GET parameter
    #path('tenders/status/'),
    #path('tenders/edit/')
]
from django.urls import path, include
from . import views

urlpatterns = [
    path('ping/', views.PingView.as_view()),
    path('tenders/', views.TenderView.as_view()),
    path('tenders/new/', views.TenderNewView.as_view()),
    path('tenders/my/', views.MyTenderView.as_view()), # GET parameter
    path('tenders/<pk>/status/', views.TenderStatusView.as_view()),
    path('tenders/<pk>/edit/', views.TenderEditView.as_view()),
    #path('/tenders/<int:pk>/rollback/<int:version>')
    path('bids/new/', views.BidNewView.as_view()),
    path('bids/my/', views.MyBidView.as_view()),
    path('bids/<pk>/list/', views.BidsByTenderView.as_view()),
    path('bids/<pk>/status/', views.BidStatusView.as_view()),
    path('bids/<pk>/edit/', views.BidEditView.as_view())
]
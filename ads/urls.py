from django.urls import path
from .views import (
    HomeView,
    AdsListView,
    AdsDetailView,
    CreateAdsView,
    ContactAdminView,
    AdsCleanupView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('ads/', AdsListView.as_view(), name='ads_list'),
    path('ads/create/', CreateAdsView.as_view(), name='ads_create'),
    path('ads/<slug:slug>/', AdsDetailView.as_view(), name='ads_detail'),
    path('contact/', ContactAdminView.as_view(), name='contact_admin'),
    path('clean/', AdsCleanupView.as_view(), name='ads_cleanup'),
]

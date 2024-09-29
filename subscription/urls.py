from django.urls import path
from subscription.apps import SubscriptionConfig
from subscription.views import SubscriptionCreateAPIView

app_name = SubscriptionConfig.name

urlpatterns = [
    path('status/', SubscriptionCreateAPIView.as_view(), name='subscription_status'),
]

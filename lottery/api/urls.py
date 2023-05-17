from django.urls import path, include
from rest_framework import routers

from .views import LotteryViewSet, TicketViewSet, LotteryWinnerAPIView, TicketBuyViewSet

router = routers.DefaultRouter()
router.register(r'lotteries', LotteryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:lottery_pk>/user/<int:user_pk>/', TicketViewSet.as_view({'get': 'list'}),
         name='ticket-list'),
    path('tickets/', TicketBuyViewSet.as_view(), name="buy-ticket"),
    path('lottery-winner/<int:ticket__lottery__id>/', LotteryWinnerAPIView.as_view(), name='lottery-winner-detail'),
]

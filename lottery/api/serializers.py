from rest_framework import serializers

from lottery.models import Lottery, Ticket, LotteryWinner


class LotterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lottery
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'lottery', 'user', 'code')

class LotteryWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LotteryWinner
        fields = '__all__'
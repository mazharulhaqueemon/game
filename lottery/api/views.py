from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from accounts.models import User
from balance.models import Balance
from lottery.api.serializers import LotterySerializer, TicketSerializer, LotteryWinnerSerializer
from lottery.models import Lottery, Ticket, LotteryWinner


class LotteryViewSet(viewsets.ModelViewSet):
    queryset = Lottery.objects.all()
    serializer_class = LotterySerializer


class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        lottery_pk = self.kwargs['lottery_pk']
        user_pk = self.kwargs['user_pk']
        return Ticket.objects.filter(lottery_id=lottery_pk, user_id=user_pk)


class TicketBuyViewSet(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request):
        user_id = request.data.get('user_id')
        lottery_id = request.data.get('lottery_id')
        no_of_tickets = request.data.get('no_of_tickets')

        try:
            user = User.objects.get(id=user_id)
            lottery = Lottery.objects.get(id=lottery_id)
            user_balance = Balance.objects.get(user=user)
        except (User.DoesNotExist, Lottery.DoesNotExist, Balance.DoesNotExist):
            return Response({"message": "User or Lottery or Balance not found."}, status=status.HTTP_404_NOT_FOUND)

        if lottery.status == 'end':
            return Response({"message": "The lottery has ended."}, status=status.HTTP_400_BAD_REQUEST)

        if no_of_tickets <= 0 or no_of_tickets > lottery.available_ticket:
            return Response({"message": "Invalid number of tickets."}, status=status.HTTP_400_BAD_REQUEST)

        ticket_price = lottery.ticket_price
        total_amount = ticket_price * no_of_tickets

        if user_balance.earn_amount < total_amount:
            return Response({"message": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        tickets = []
        for _ in range(no_of_tickets):
            ticket = Ticket.objects.create(lottery=lottery, user=user)
            tickets.append(ticket)

        user_balance.earn_amount -= total_amount
        user_balance.save()

        lottery.available_ticket -= no_of_tickets
        lottery.save()

        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LotteryWinnerAPIView(generics.RetrieveAPIView):
    queryset = LotteryWinner.objects.all()
    serializer_class = LotteryWinnerSerializer
    lookup_field = 'ticket__lottery__id'

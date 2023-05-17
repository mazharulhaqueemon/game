from django.contrib import admin

from lottery.models import Lottery, Ticket, LotteryWinner

# Register your models here.
admin.site.register(Lottery)
admin.site.register(Ticket)
admin.site.register(LotteryWinner)
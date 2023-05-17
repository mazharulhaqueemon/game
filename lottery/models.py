import uuid

from django.db import models

from accounts.models import User


class Lottery(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField(max_length=500)
    banner = models.ImageField(upload_to='lottery_banners/')
    total_ticket = models.PositiveIntegerField()
    available_ticket = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=(
        ('running', 'Running'),
        ('end', 'End'),
    ))

    def __str__(self):
        return self.title


class Ticket(models.Model):
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE, related_name="lottery_ticket")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        code = str(uuid.uuid4())[:6].upper()
        while Ticket.objects.filter(code=code).exists():
            code = str(uuid.uuid4())[:6].upper()
        return code

    def __str__(self):
        return self.code


class LotteryWinner(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name="ticket_winner")
    prize = models.CharField(max_length=255)

    def __str__(self):
        return f"Winner: {self.ticket.user.get_full_name()}, Prize: {self.prize}"

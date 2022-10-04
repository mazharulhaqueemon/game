# Generated by Django 3.2 on 2022-09-30 06:09

import balance.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.CharField(blank=True, max_length=80, null=True, unique=True)),
                ('logo', models.ImageField(upload_to=balance.models.payment_method_logo_path)),
                ('account_number', models.CharField(max_length=50)),
                ('percent_charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('is_receive_transaction_id', models.BooleanField(default=True)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Payment Methods',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WithdrawRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('receiver_number', models.CharField(max_length=50)),
                ('is_pending', models.BooleanField(default=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('is_declined', models.BooleanField(default=False)),
                ('requested_datetime', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='balance.paymentmethod')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Withdraw Requests',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DepositRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot', models.ImageField(upload_to=balance.models.deposit_screenshot_image_path)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sender_number', models.CharField(max_length=50)),
                ('transaction_id', models.CharField(blank=True, max_length=50, null=True)),
                ('is_pending', models.BooleanField(default=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('is_declined', models.BooleanField(default=False)),
                ('requested_datetime', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='balance.paymentmethod')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Deposit Requests',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('updated_datetime', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Balance',
                'ordering': ['-id'],
            },
        ),
    ]

# Generated by Django 3.1 on 2020-08-25 12:12

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
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='StockOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='place_order', to=settings.AUTH_USER_MODEL)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock_order', to='stocks.stock')),
            ],
        ),
    ]

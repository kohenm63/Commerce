# Generated by Django 3.2.8 on 2021-12-14 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20211214_0820'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='item',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auction_listings'),
        ),
    ]

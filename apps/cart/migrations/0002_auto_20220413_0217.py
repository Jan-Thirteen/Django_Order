# Generated by Django 2.2 on 2022-04-12 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='cart.Order'),
        ),
    ]

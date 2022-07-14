# Generated by Django 3.1.5 on 2022-07-11 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_photo'),
        ('order', '0004_ordertransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='shop.item'),
        ),
        migrations.DeleteModel(
            name='OrderTransaction',
        ),
    ]

# Generated by Django 3.1.5 on 2022-07-15 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20220711_1048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='price',
            new_name='item_price',
        ),
        migrations.AddField(
            model_name='order',
            name='notice',
            field=models.CharField(max_length=150, null=True, verbose_name='배송시 유의사항'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='order.order'),
        ),
        migrations.CreateModel(
            name='OrderTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_order_id', models.CharField(blank=True, max_length=120, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=120, null=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('transaction_status', models.CharField(blank=True, max_length=220, null=True)),
                ('type', models.CharField(blank=True, max_length=120)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]

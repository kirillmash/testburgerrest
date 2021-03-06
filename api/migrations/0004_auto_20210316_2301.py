# Generated by Django 3.1.7 on 2021-03-16 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210316_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishesinorder',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dish', to='api.dish'),
        ),
        migrations.AlterField(
            model_name='dishesinorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='api.order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='dishes',
            field=models.ManyToManyField(related_name='dishes', through='api.DishesInOrder', to='api.Dish'),
        ),
        migrations.AlterField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='api.restaurant'),
        ),
    ]

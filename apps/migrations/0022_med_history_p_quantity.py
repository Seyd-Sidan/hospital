# Generated by Django 4.0.1 on 2022-02-08 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0021_products_quantity_products_warning'),
    ]

    operations = [
        migrations.AddField(
            model_name='med_history',
            name='p_quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

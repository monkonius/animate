# Generated by Django 4.2.3 on 2023-07-27 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]

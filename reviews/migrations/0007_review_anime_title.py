# Generated by Django 4.2.3 on 2023-09-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_review_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='anime_title',
            field=models.CharField(default='Placeholder', max_length=256),
            preserve_default=False,
        ),
    ]
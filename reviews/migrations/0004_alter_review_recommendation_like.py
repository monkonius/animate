# Generated by Django 4.2.3 on 2023-08-07 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='recommendation',
            field=models.CharField(choices=[('RE', 'Recommended'), ('MF', 'Mixed Feelings'), ('NR', 'Not Recommended')], default=None, max_length=2),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='reviews.review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

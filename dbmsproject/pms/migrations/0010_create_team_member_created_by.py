# Generated by Django 3.2.25 on 2024-05-22 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pms', '0009_remove_create_team_member_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='create_team_member',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_team_members', to=settings.AUTH_USER_MODEL),
        ),
    ]

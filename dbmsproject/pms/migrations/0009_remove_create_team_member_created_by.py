# Generated by Django 3.2.25 on 2024-05-22 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0008_alter_create_team_member_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='create_team_member',
            name='created_by',
        ),
    ]

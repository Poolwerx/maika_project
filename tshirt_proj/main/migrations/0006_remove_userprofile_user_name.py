# Generated by Django 4.1.4 on 2023-04-23 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_userprofile_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_name',
        ),
    ]
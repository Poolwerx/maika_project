# Generated by Django 4.1.4 on 2023-04-18 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userprofile_about_userprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]

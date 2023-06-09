# Generated by Django 4.1.4 on 2023-04-26 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0011_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='images/def_logo.jpg', upload_to='user_profiles/')),
            ],
        ),
        migrations.CreateModel(
            name='UserItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(default='', max_length=20)),
                ('category', models.CharField(default='', max_length=20)),
                ('description', models.TextField(default='')),
                ('pictures', models.ManyToManyField(to='main.image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

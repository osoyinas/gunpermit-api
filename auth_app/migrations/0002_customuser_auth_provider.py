# Generated by Django 5.0.1 on 2024-11-03 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='auth_provider',
            field=models.CharField(default='email', max_length=255),
        ),
    ]

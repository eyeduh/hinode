# Generated by Django 3.2.7 on 2021-09-16 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_date_of_birth'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]

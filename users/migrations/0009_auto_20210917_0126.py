# Generated by Django 3.2.7 on 2021-09-16 20:56

from django.db import migrations, models
import django.db.models.deletion
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210917_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='is admin'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='media/avatars', verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='bio'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(validators=[users.validators.MinAgeValidator], verbose_name='date of birth'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following', to='users.User', verbose_name='followers'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Female'), (2, 'Male'), (3, 'Rather Not Say')], default=1, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='job',
            field=models.CharField(max_length=100, verbose_name='job'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='nickname'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.PositiveBigIntegerField(unique=True, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='updated'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='user'),
        ),
    ]

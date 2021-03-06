# Generated by Django 3.2.7 on 2021-09-17 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nodes', '0006_alter_node_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='comments',
            field=models.ManyToManyField(related_name='node_user_comment', through='nodes.NodeComment', to=settings.AUTH_USER_MODEL, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='node',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='node_user_like', through='nodes.NodeLike', to=settings.AUTH_USER_MODEL, verbose_name='likes'),
        ),
        migrations.AlterField(
            model_name='node',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='nodecomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='nodelike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]

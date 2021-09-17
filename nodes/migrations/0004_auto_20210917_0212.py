# Generated by Django 3.2.7 on 2021-09-16 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210917_0126'),
        ('nodes', '0003_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='node',
            options={'ordering': ['-id'], 'verbose_name': 'Node', 'verbose_name_plural': 'Nodes'},
        ),
        migrations.AlterField(
            model_name='node',
            name='comments',
            field=models.ManyToManyField(related_name='node_user_comment', through='nodes.NodeComment', to='users.User', verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='node',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='node',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/images/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='node',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='node_user_like', through='nodes.NodeLike', to='users.User', verbose_name='likes'),
        ),
        migrations.AlterField(
            model_name='node',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nodes.node', verbose_name='parent'),
        ),
        migrations.AlterField(
            model_name='node',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='node',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='users.user', verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='nodecomment',
            name='content',
            field=models.CharField(max_length=200, verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='nodecomment',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nodes.node', verbose_name='node'),
        ),
        migrations.AlterField(
            model_name='nodecomment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='nodecomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='nodelike',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nodes.node', verbose_name='node'),
        ),
        migrations.AlterField(
            model_name='nodelike',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='nodelike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='user'),
        ),
        migrations.AlterModelTable(
            name='node',
            table='nodes',
        ),
    ]
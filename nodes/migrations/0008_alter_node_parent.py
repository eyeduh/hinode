# Generated by Django 3.2.7 on 2021-09-17 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0007_auto_20210917_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nodes.node', verbose_name='parent'),
        ),
    ]

# Generated by Django 3.2.7 on 2021-09-18 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contactApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='Master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contactApp.master'),
            preserve_default=False,
        ),
    ]
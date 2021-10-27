# Generated by Django 3.2.7 on 2021-09-25 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactApp', '0004_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='Country',
            field=models.CharField(choices=[('in', 'India'), ('us', 'United States'), ('uk', 'United Kingdom')], max_length=20),
        ),
    ]

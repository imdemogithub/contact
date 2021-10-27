# Generated by Django 3.2.7 on 2021-09-25 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contactApp', '0003_auto_20210921_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(choices=[('fm', 'Family'), ('bs', 'Business'), ('fr', 'Friends')], max_length=10)),
                ('FullName', models.CharField(default='', max_length=50)),
                ('Email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('Mobile', models.CharField(default='', max_length=10, null=True)),
                ('Country', models.CharField(default='', max_length=25, null=True)),
                ('Pincode', models.CharField(default='', max_length=6, null=True)),
                ('Address', models.TextField(default='', max_length=100, null=True)),
                ('UserProfile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contactApp.userprofile')),
            ],
        ),
    ]

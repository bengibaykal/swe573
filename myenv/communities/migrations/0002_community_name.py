# Generated by Django 2.2.6 on 2019-10-31 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='name',
            field=models.CharField(default='null', max_length=200),
        ),
    ]

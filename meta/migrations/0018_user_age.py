# Generated by Django 3.0.3 on 2020-12-14 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0017_auto_20201028_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
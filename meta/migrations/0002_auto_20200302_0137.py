# Generated by Django 3.0.3 on 2020-03-02 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='downloaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='album',
            name='publish_year',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
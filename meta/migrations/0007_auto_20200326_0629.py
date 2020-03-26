# Generated by Django 3.0.3 on 2020-03-25 22:29
import core.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0006_song_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
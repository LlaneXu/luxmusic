# Generated by Django 3.0.3 on 2020-10-28 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0015_comment_replied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='replied',
            field=models.ManyToManyField(blank=True, related_name='_comment_replied_+', to='meta.Comment'),
        ),
    ]
# Generated by Django 3.0.3 on 2020-11-05 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_auto_20201028_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyzeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(db_index=True, max_length=16)),
                ('tag', models.CharField(max_length=16)),
                ('counts', models.BigIntegerField(default=0)),
            ],
        ),
    ]

# Generated by Django 4.0.1 on 2022-01-28 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('api_id', models.CharField(max_length=9)),
                ('api_hash', models.CharField(max_length=32)),
            ],
        ),
    ]

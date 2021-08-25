# Generated by Django 3.2.6 on 2021-08-25 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=1000)),
                ('thumbnails_url', models.URLField()),
                ('publishing_datetime', models.DateTimeField()),
            ],
            options={
                'ordering': ('-publishing_datetime',),
            },
        ),
    ]

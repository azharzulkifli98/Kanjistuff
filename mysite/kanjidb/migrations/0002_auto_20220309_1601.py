# Generated by Django 3.1.4 on 2022-03-09 22:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanjidb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='date_created',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='tag',
            name='last_updated',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='tag',
            name='num_kanji_included',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(max_length=30),
        ),
        migrations.CreateModel(
            name='Kanji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kanji_id', models.CharField(max_length=20)),
                ('kanji_name', models.CharField(max_length=30)),
                ('kanji_description', models.CharField(max_length=255)),
                ('kanji_api_info', models.URLField()),
                ('num_tags_included', models.PositiveIntegerField(default=1)),
                ('date_created', models.DateTimeField(default=datetime.date.today)),
                ('last_updated', models.DateTimeField(default=datetime.date.today)),
                ('list_tags_included', models.ManyToManyField(to='kanjidb.Tag')),
            ],
        ),
    ]

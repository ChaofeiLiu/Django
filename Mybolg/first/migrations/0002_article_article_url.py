# Generated by Django 2.1.5 on 2020-08-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_url',
            field=models.CharField(default='', max_length=100, verbose_name='文章网址'),
        ),
    ]
# Generated by Django 5.1.3 on 2024-12-10 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0009_alter_reply_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='content',
        ),
    ]

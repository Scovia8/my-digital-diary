# Generated by Django 5.1.3 on 2024-12-05 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0004_alter_comment_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='active',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='slug',
        ),
    ]
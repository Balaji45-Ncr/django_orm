# Generated by Django 4.2.11 on 2025-05-14 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_alter_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.6 on 2023-03-31 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generateTest', '0009_test_accepting_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='mutli_response',
            field=models.BooleanField(default=False),
        ),
    ]

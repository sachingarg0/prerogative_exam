# Generated by Django 4.0.6 on 2023-03-23 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generateTest', '0002_student_test_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='test_id',
        ),
    ]
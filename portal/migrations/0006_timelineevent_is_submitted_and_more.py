# Generated by Django 4.2.8 on 2025-02-22 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_timelineevent_assessment_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelineevent',
            name='is_submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timelineevent',
            name='submission_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timelineevent',
            name='submission_file',
            field=models.FileField(blank=True, null=True, upload_to='submissions/'),
        ),
        migrations.AddField(
            model_name='timelineevent',
            name='submission_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]

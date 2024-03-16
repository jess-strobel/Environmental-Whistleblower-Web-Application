# Generated by Django 5.0.2 on 2024-03-15 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whistleblowingapp', '0002_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='attachment',
        ),
        migrations.RemoveField(
            model_name='report',
            name='description',
        ),
        migrations.RemoveField(
            model_name='report',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='report',
            name='title',
        ),
        migrations.AddField(
            model_name='report',
            name='reportDescription',
            field=models.TextField(default=''),
        ),
        # migrations.AddField(
        #     model_name='report',
        #     name='reportJPEG',
        #     field=models.ImageField(blank=True, null=True, upload_to='report_image/'),
        # ),
        # migrations.AddField(
        #     model_name='report',
        #     name='reportPDF',
        #     field=models.FileField(blank=True, null=True, upload_to='report_pdf/'),
        # ),
        # migrations.AddField(
        #     model_name='report',
        #     name='reportText',
        #     field=models.FileField(blank=True, null=True, upload_to='report_txt/'),
        # ),
        # migrations.AddField(
        #     model_name='report',
        #     name='reportTitle',
        #     field=models.CharField(default='', max_length=255),
        # ),
    ]

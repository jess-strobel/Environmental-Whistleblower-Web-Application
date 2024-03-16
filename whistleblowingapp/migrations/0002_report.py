# Generated by Django 5.0.2 on 2024-03-15 01:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whistleblowingapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),

    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('file_type', models.CharField(choices=[('txt', 'Text File'), ('pdf', 'PDF'), ('jpg', 'JPEG Image')], max_length=3)),
                ('attachment', models.FileField(upload_to='report_attachments/')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reportTitle', models.CharField(max_length=255)),
                ('reportText', models.TextField()),
                ('reportPDF', models.FileField(upload_to='report_pdf/')),
                ('reportJPEG', models.ImageField(upload_to='report_image/')),

            ],
        ),
    ]

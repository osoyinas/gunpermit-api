# Generated by Django 4.2.7 on 2023-11-22 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_files_app', '0007_pdffile_created_at_alter_pdffile_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdffile',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]

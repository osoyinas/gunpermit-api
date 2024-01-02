# Generated by Django 4.2.7 on 2023-11-21 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions_app', '0007_alter_questionmodel_subtopic_and_more'),
        ('pdf_files_app', '0004_alter_pdffile_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdffile',
            name='topic',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='questions_app.topicmodel'),
            preserve_default=False,
        ),
    ]

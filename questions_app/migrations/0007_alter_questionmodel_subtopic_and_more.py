# Generated by Django 4.2.7 on 2023-11-21 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions_app', '0006_alter_questionmodel_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionmodel',
            name='subtopic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='questions_app.subtopicmodel'),
        ),
        migrations.AlterField(
            model_name='questionmodel',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='questions_app.topicmodel'),
        ),
    ]

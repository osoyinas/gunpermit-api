# Generated by Django 5.0.1 on 2024-09-20 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions_app', '0001_initial'),
        ('quizzes_app', '0002_rename_quizquestion_quizquestionmodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizmodel',
            name='questions',
            field=models.ManyToManyField(default=[], through='quizzes_app.QuizQuestionModel', to='questions_app.questionmodel'),
        ),
    ]

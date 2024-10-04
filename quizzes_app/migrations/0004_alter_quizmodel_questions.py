# Generated by Django 5.0.1 on 2024-09-20 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions_app', '0001_initial'),
        ('quizzes_app', '0003_alter_quizmodel_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizmodel',
            name='questions',
            field=models.ManyToManyField(through='quizzes_app.QuizQuestionModel', to='questions_app.questionmodel'),
        ),
    ]
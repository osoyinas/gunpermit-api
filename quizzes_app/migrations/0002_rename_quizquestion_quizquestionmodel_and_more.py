# Generated by Django 5.0.1 on 2024-09-19 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions_app', '0001_initial'),
        ('quizzes_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuizQuestion',
            new_name='QuizQuestionModel',
        ),
        migrations.RenameField(
            model_name='quizquestionmodel',
            old_name='test',
            new_name='quiz',
        ),
        migrations.AlterUniqueTogether(
            name='quizquestionmodel',
            unique_together={('quiz', 'question')},
        ),
    ]
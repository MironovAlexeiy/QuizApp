# Generated by Django 4.1.4 on 2022-12-26 10:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizapp', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='users',
            field=models.ManyToManyField(related_name='quizzes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_quiz', to=settings.AUTH_USER_MODEL),
        ),
    ]
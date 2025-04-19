# Generated by Django 5.1.7 on 2025-04-19 19:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_alter_profile_experianse_level_alter_profile_gender_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('exercise_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('muscle_group', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
                ('sets', models.IntegerField()),
                ('reps', models.IntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.exercise')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Program_maker', to='accounts.profile')),
                ('exercises', models.ManyToManyField(related_name='programs', through='exercises.ExerciseSchedule', to='exercises.exercise')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Program_assigned', to='accounts.profile')),
            ],
        ),
        migrations.AddField(
            model_name='exerciseschedule',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.program'),
        ),
        migrations.AlterUniqueTogether(
            name='exerciseschedule',
            unique_together={('exercise', 'program', 'day')},
        ),
    ]

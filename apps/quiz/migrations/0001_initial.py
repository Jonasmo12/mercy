# Generated by Django 3.1.7 on 2021-06-19 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('section', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('numberOfQuestions', models.IntegerField(verbose_name='Number Of Questions')),
                ('passScore', models.IntegerField(verbose_name='Pass Percentage')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(null=True)),
                ('createdBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.teacher')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='section.section')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.subject')),
            ],
            options={
                'verbose_name_plural': 'Quizess',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('quiz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.quiz')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='section.section')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.student')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.subject')),
            ],
        ),
    ]

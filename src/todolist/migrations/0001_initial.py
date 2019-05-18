# Generated by Django 2.1 on 2019-05-18 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='할 일 제목')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('modify_date', models.DateField(auto_now=True)),
                ('done', models.BooleanField(default=False, verbose_name='완료 시 선택해주세요')),
                ('description', models.CharField(blank=True, max_length=50, verbose_name='내용')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='마감 기한')),
                ('priority', models.CharField(choices=[('1', '낮음'), ('2', '중간'), ('3', '높음')], default='1', max_length=1, verbose_name='우선 순위')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['done', '-priority', 'deadline'],
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='목록 이름')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('modify_date', models.DateField(auto_now=True)),
                ('done', models.BooleanField(default=False, verbose_name='완료 시 선택해주세요')),
                ('description', models.CharField(blank=True, max_length=50, verbose_name='내용')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='마감 기한')),
                ('priority', models.CharField(choices=[('1', '낮음'), ('2', '중간'), ('3', '높음')], default='1', max_length=1, verbose_name='우선 순위')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['done', '-priority', 'deadline'],
            },
        ),
        migrations.AddField(
            model_name='card',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.Work'),
        ),
    ]

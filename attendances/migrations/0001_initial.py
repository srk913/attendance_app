# Generated by Django 3.1.2 on 2020-10-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_id', models.IntegerField(verbose_name='Attendance ID')),
                ('work_type', models.IntegerField(choices=[(1, 'SES'), (2, '派遣'), (3, '社内業務'), (4, '出勤予定'), (5, '受託'), (6, '内勤')], verbose_name='種別')),
                ('opening_time', models.TimeField(verbose_name='始業時間')),
                ('closing_time', models.TimeField(verbose_name='終業時間')),
                ('break_time', models.TimeField(verbose_name='休憩時間')),
                ('date', models.DateField(verbose_name='日付')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

# Generated by Django 3.1.3 on 2021-05-14 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210513_2220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='TeacherName',
        ),
        migrations.AddField(
            model_name='user',
            name='TeacherClass',
            field=models.CharField(default=1, max_length=15, verbose_name='管理班级号'),
            preserve_default=False,
        ),
    ]

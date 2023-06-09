# Generated by Django 4.0.4 on 2023-03-16 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(db_index=True, help_text='学号最大长度为30', max_length=30, unique=True, verbose_name='学号')),
                ('student_name', models.CharField(db_index=True, help_text='学号最大长度为30', max_length=30, verbose_name='姓名')),
                ('student_sex', models.SmallIntegerField(choices=[(1, '男'), (0, '女')], help_text='1->男,0->女', verbose_name='性别')),
                ('student_birthday', models.DateField(help_text='学生生日', verbose_name='生日')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'db_table': 't_student',
            },
        ),
    ]

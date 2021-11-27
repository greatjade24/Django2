# Generated by Django 2.1.5 on 2021-11-25 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('제목', models.CharField(max_length=255)),
                ('작성자', models.CharField(max_length=255)),
                ('내용', models.TextField()),
                ('작성일', models.DateTimeField()),
                ('수정일', models.DateTimeField()),
                ('조회수', models.IntegerField()),
            ],
        ),
    ]

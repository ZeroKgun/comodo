# Generated by Django 3.2.5 on 2021-12-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0004_auto_20180501_0436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judgeserver',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

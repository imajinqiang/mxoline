# Generated by Django 2.2.5 on 2019-10-14 18:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_auto_20190812_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='is_auth',
            field=models.BooleanField(default=False, verbose_name='是否认证'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='is_gold',
            field=models.BooleanField(default=False, verbose_name='是否金牌'),
        ),
        migrations.AlterField(
            model_name='city',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=10, verbose_name='城市名称'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('institutions', '培训机构'), ('personal', '个人'), ('universities', '高校')], max_length=20, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
    ]
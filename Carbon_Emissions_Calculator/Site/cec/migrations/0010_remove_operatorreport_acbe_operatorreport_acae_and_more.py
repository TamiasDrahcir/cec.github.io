# Generated by Django 5.1 on 2024-11-02 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cec', '0009_rename_acb_operatorreport_aca_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operatorreport',
            name='ACBE',
        ),
        migrations.AddField(
            model_name='operatorreport',
            name='ACAE',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='operatorreport',
            name='ALL_ELE',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='ACA',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='ACAA',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='ACAL',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='GYM',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='GYME',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='GYML',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='RES',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='RESA',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='RESE',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='RESL',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='SCI',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='SCIA',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='SCIE',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='SCIL',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='THE',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='THEA',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='THEE',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='operatorreport',
            name='THEL',
            field=models.IntegerField(default=0),
        ),
    ]

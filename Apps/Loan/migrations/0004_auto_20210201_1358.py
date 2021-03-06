# Generated by Django 3.1.5 on 2021-02-01 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loan', '0003_auto_20210201_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loaninfo',
            name='exit_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='loaninfo',
            name='interest_per_day',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loaninfo',
            name='rate_of_interest',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loaninfo',
            name='sr_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loaninfo',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.1.5 on 2021-02-03 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loan', '0005_auto_20210203_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loaninfo',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

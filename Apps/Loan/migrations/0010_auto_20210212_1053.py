# Generated by Django 3.1.5 on 2021-02-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loan', '0009_loandetail_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loandetail',
            name='Notes',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
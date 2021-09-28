# Generated by Django 3.1.5 on 2021-03-17 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Loan', '0015_auto_20210317_1018'),
    ]

    operations = [
        migrations.CreateModel(
            name='SerialNo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='loaninfo',
            name='sr_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sr_no_master', to='Loan.serialno'),
        ),
    ]

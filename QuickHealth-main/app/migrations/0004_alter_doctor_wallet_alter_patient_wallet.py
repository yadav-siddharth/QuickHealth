# Generated by Django 4.0.4 on 2022-04-29 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_doctor_wallet_patient_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='Wallet',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='Wallet',
            field=models.BigIntegerField(default=0),
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-02 16:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signInSignUp', '0004_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='user_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='signInSignUp.users'),
        ),
    ]

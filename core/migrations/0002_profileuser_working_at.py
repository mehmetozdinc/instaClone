# Generated by Django 4.2.5 on 2023-09-06 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileuser',
            name='working_at',
            field=models.CharField(default='#', max_length=150, null=True),
        ),
    ]

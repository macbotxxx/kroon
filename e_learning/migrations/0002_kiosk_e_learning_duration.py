# Generated by Django 3.2.9 on 2022-06-02 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_learning', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kiosk_e_learning',
            name='duration',
            field=models.CharField(blank=True, help_text='This hold the current video duration of the e-Learning process.', max_length=255, null=True, verbose_name='Video Duration'),
        ),
    ]
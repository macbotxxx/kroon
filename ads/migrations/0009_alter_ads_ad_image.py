# Generated by Django 3.2.9 on 2022-05-19 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0008_ads_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='ad_image',
            field=models.ImageField(help_text='input ad image which will be JPEG, PNG, or GIF', max_length=250, null=True, upload_to='ads_images/', verbose_name='Ad Image'),
        ),
    ]

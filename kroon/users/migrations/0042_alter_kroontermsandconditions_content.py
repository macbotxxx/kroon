# Generated by Django 3.2.9 on 2022-01-13 22:26

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0041_kroontermsandconditions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kroontermsandconditions',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
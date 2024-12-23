# Generated by Django 3.2.9 on 2022-03-10 07:28

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0066_policyandcondition'),
    ]

    operations = [
        migrations.CreateModel(
            name='KroonFQA',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('question', models.CharField(help_text='the questions which customers are likely to ask or know about.', max_length=255, null=True, verbose_name='Question')),
                ('answer', models.TextField(help_text='The answer to the question been provided for the customer satisfaction', null=True, verbose_name='Answer')),
            ],
            options={
                'verbose_name': 'Kroon FQAs',
                'verbose_name_plural': 'Kroon FQAs',
                'ordering': ('-created_date',),
            },
        ),
    ]

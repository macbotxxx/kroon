# Generated by Django 3.2.9 on 2022-03-07 21:47

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsFeed',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='The unique identifier of an object.', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Timestamp when the record was created.', max_length=20, verbose_name='Created Date')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, help_text='Modified date when the record was created.', max_length=20, verbose_name='Modified Date')),
                ('title', models.CharField(help_text='The title of the new feed that will be displayed to the user', max_length=255, null=True, verbose_name='News Feed Title')),
                ('image', models.ImageField(blank=True, help_text='news feed image that will be displayed to the user', null=True, upload_to='news_feed/', verbose_name='News Feed Image')),
                ('content', models.TextField(help_text='this holds the content of the news feed', null=True, verbose_name='News Feed Content')),
                ('status', models.BooleanField(default=False, help_text='news feed status which determines whether the feed should be shown or not', null=True, verbose_name='News Feed Status')),
            ],
            options={
                'verbose_name': 'News Feed',
                'verbose_name_plural': 'News Feed',
                'ordering': ('-created_date',),
            },
        ),
    ]
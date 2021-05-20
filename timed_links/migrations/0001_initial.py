# Generated by Django 3.0.10 on 2021-05-20 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimedLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(blank=True, help_text='The part of the URL after the /', max_length=32, null=True, unique=True)),
                ('open_time', models.DateTimeField(help_text='The time at which the link should be opened.')),
                ('close_time', models.DateTimeField(help_text='The time at which the link should be closed.')),
                ('redirect_url', models.CharField(help_text='The URL the link will redirect to, while it is open.', max_length=256)),
                ('message_when_too_early', models.TextField(help_text='The message to be shown, when the link has been opened before the open time was reached.')),
                ('message_on_homepage', models.TextField(help_text='The message to be shown on the homepage while the link is open.')),
                ('message_when_too_late', models.TextField(help_text='The message to be shown, when the link has been opened after the close time was reached.')),
                ('button_text', models.CharField(help_text='The text on the button', max_length=128)),
                ('number_of_requests', models.IntegerField(editable=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('modified_at', models.DateTimeField(editable=False)),
            ],
        ),
    ]

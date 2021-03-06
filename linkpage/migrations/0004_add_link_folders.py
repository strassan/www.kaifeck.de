# Generated by Django 3.0.11 on 2021-05-14 09:46

from django.db import migrations, models
import django.db.models.deletion


def switch_to_linkfolder(apps, schema_editor):
    old_link = apps.get_model('linkpage', 'OldLink')
    new_link = apps.get_model('linkpage', 'NewLink')
    linkfolder = apps.get_model('linkpage', 'LinkFolder')

    for link in old_link.objects.all():
        linkfolder_object = linkfolder.objects.create(
            title=link.title,
            description=link.description,
            image=link.image,
            open_date=link.open_date,
            close_date=link.close_date,
            created_at=link.created_at,
            modified_at=link.modified_at,
        )
        linkfolder_object.save()
        new_link_object = new_link.objects.create(
            linkfolder_ptr=linkfolder_object,
            url=link.url,
            alt_url=link.alt_url,
            parent_folder=None
        )
        new_link_object.save()
        link.delete()


def switch_to_no_linkfolder(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('linkpage', '0003_link_alt_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(help_text='For best result, always upload images with 1:1 aspect ratio', upload_to='links')),
                ('open_date', models.DateField(blank=True, help_text='The first day on which the link will be visible on the linkpage', null=True)),
                ('close_date', models.DateField(blank=True, help_text='The last day on which the link will be visible on the linkpage', null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('modified_at', models.DateTimeField(editable=False)),
            ],
        ),
        migrations.RenameModel('Link', 'OldLink'),
        migrations.CreateModel(
            name='NewLink',
            fields=[
                ('linkfolder_ptr', models.OneToOneField(
                    auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True, primary_key=True, serialize=False, to='linkpage.LinkFolder'
                )),
                ('url', models.CharField(max_length=256)),
                ('alt_url', models.CharField(
                    max_length=256,
                    verbose_name="Alternative Url",
                    help_text="Provide an alternative url, if original url does not use http or https protocol",
                    null=True, blank=True
                )),
                ('parent_folder', models.ForeignKey(
                    blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                    related_name='+', to='linkpage.LinkFolder'
                ))
            ],
        ),
        migrations.RunPython(switch_to_linkfolder),
        migrations.DeleteModel('OldLink'),
        migrations.RenameModel('NewLink', 'Link')
    ]

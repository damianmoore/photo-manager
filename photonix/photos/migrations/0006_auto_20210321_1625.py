# Generated by Django 3.0.7 on 2021-03-21 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0005_auto_20210206_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photofile',
            name='preferred',
        ),
        migrations.AddField(
            model_name='photo',
            name='preferred_photo_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='photos.PhotoFile'),
        ),
        migrations.AddField(
            model_name='photo',
            name='thumbnailed_version',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='photofile',
            name='thumbnailed_version',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='phototag',
            name='model_version',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

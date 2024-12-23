# Generated by Django 5.0.6 on 2024-07-18 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0014_alter_message_options_alter_profile_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to='media_files/'),
        ),
        migrations.AddField(
            model_name='message',
            name='media_image',
            field=models.ImageField(blank=True, null=True, upload_to='media_images/'),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]

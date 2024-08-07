# Generated by Django 5.0.6 on 2024-07-17 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0013_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={},
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(blank=True, default='profile_photos/default-user-image.png', null=True, upload_to='profile_photos/'),
        ),
    ]

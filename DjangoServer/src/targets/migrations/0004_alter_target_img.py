# Generated by Django 4.0.3 on 2022-03-24 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0003_target_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='img',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]
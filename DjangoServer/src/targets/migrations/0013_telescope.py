# Generated by Django 4.0.3 on 2022-05-10 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0012_alter_deepspacetarget_bayer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Telescope',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.CharField(max_length=10)),
                ('baud_rate', models.IntegerField()),
                ('cur_alt', models.DecimalField(decimal_places=5, max_digits=10)),
                ('cur_az', models.DecimalField(decimal_places=5, max_digits=10)),
            ],
        ),
    ]

# Generated by Django 4.1.5 on 2023-04-11 20:41

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.UploadFile.upload_to, verbose_name='تصویر پروفایل'),
        ),
    ]

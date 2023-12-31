# Generated by Django 4.2.7 on 2023-12-16 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='doctor',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='doctor',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='creator',
            field=models.CharField(default='manager1', max_length=255),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='doctor_profile_pics/'),
        ),
    ]

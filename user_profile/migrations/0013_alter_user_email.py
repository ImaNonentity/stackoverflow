# Generated by Django 4.0.5 on 2022-06-14 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0012_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50, unique=True, verbose_name='email'),
        ),
    ]
# Generated by Django 4.0.5 on 2022-06-10 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.SmallIntegerField(blank=True, default=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('N', 'Newbie'), ('A', 'Apprentice'), ('T', 'Thinker'), ('M', 'Master'), ('G', 'Genius'), ('H', 'Higher Intelligence')], default='Newbie', max_length=20, verbose_name='user title'),
        ),
    ]

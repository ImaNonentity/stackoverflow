# Generated by Django 4.0.5 on 2022-06-14 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='username',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='type',
        ),
        migrations.AddField(
            model_name='vote',
            name='action_type',
            field=models.CharField(choices=[('1', 1), ('0', 0), ('-1', -1)], default=0, max_length=20),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-07 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_rename_username_answer_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='social.tag', verbose_name='User tag(s)'),
        ),
    ]

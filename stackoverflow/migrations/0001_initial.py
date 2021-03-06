# Generated by Django 4.0.5 on 2022-06-02 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='answered')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='edited')),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField(blank=True, max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Asked')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Modified')),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=200, unique=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('avatar', models.ImageField(upload_to='')),
                ('email', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('full_name', models.CharField(max_length=200)),
                ('role', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField()),
                ('email_confirmation', models.BooleanField(default=False)),
                ('rating', models.SmallIntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('UP_VOTE', 1), ('DOWN_VOTE', -1)], max_length=50)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stackoverflow.answer')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stackoverflow.question')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stackoverflow.user')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='stackoverflow.tag', verbose_name='User`s tag(s)'),
        ),
        migrations.AddField(
            model_name='question',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stackoverflow.user'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('likes', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='answered')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='edited')),
                ('object_id', models.PositiveIntegerField()),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stackoverflow.answer')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stackoverflow.question')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stackoverflow.user')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stackoverflow.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stackoverflow.user'),
        ),
    ]

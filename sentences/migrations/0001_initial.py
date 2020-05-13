# Generated by Django 3.0.5 on 2020-04-25 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Sentence number in text')),
                ('content', models.TextField(verbose_name='Sentence text')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sentences.Text')),
            ],
            options={
                'ordering': ['number'],
                'unique_together': {('number', 'text')},
            },
        ),
    ]

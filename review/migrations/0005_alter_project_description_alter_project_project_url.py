# Generated by Django 4.0.4 on 2022-06-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_url',
            field=models.CharField(max_length=1000),
        ),
    ]

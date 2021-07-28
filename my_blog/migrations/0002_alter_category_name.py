# Generated by Django 3.2.4 on 2021-07-27 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Food', 'Food'), ('Travel', 'Travel'), ('Music', 'Music'), ('Lifestyle', 'Lifestyle'), ('Fitness', 'Fitness'), ('Sports', 'Sports')], max_length=25, unique=True),
        ),
    ]

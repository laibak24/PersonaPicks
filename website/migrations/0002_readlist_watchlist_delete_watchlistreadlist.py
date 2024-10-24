# Generated by Django 5.1.2 on 2024-10-24 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Readlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('books', models.ManyToManyField(related_name='readlist', to='website.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.user')),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('movies', models.ManyToManyField(related_name='watchlist', to='website.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.user')),
            ],
        ),
        migrations.DeleteModel(
            name='WatchlistReadlist',
        ),
    ]

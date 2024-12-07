# Generated by Django 5.1.3 on 2024-12-02 08:54

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MBTIType',
            fields=[
                ('mbti_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('mbti_type', models.CharField(choices=[('INTJ', 'INTJ'), ('INTP', 'INTP'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'), ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'), ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'), ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP')], max_length=4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default='', max_length=150, unique=True)),
                ('email', models.EmailField(default='', max_length=254, unique=True)),
                ('avatar', models.ImageField(default='avatar.svg', null=True, upload_to='avatars/')),
                ('bio', models.TextField(blank=True, default='Tell others about yourself!')),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('mbti_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.mbtitype')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ActivityFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('feedback_giver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('publication_year', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(default='default_book.jpg', upload_to='book_images/')),
                ('first_preference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preferred_books_first', to='website.mbtitype')),
                ('second_preference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preferred_books_second', to='website.mbtitype')),
                ('third_preference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preferred_books_third', to='website.mbtitype')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(default='default_movie.jpg', upload_to='media/movie_images/')),
                ('first_preference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preferred_movies_first', to='website.mbtitype')),
                ('second_preference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preferred_movies_second', to='website.mbtitype')),
                ('third_preference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preferred_movies_third', to='website.mbtitype')),
            ],
        ),
        migrations.CreateModel(
            name='Readlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('readlist_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReadlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='not_started', max_length=20)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readlist_items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('recommendation_id', models.AutoField(primary_key=True, serialize=False)),
                ('recommended_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.book')),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.movie')),
                ('recommendation_for_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('watchlist_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WatchlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='not_started', max_length=20)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompatibilityScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('compared_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compared_scores', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compatibility_scores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'compared_user')},
            },
        ),
    ]

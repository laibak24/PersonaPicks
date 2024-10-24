from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# MBTI Type Model
class MBTIType(models.Model):
    mbti_type_id = models.AutoField(primary_key=True)
    mbti_type = models.CharField(max_length=255)

    def __str__(self):
        return self.mbti_type

# User Manager for handling user creation
class UserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None, mbti_type=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not user_name:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
            mbti_type=mbti_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password=None, mbti_type=None):
        user = self.create_user(
            email=email,
            user_name=user_name,
            password=password,
            mbti_type=mbti_type,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# User Model
class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    mbti_type = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name

# Movie Model
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

# Book Model
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    publication_year = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

# Song Model
class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    album = models.CharField(max_length=255, blank=True)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

# Feedback Model
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user}"

# Recommendations Model
class Recommendation(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True)
    recommended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.user}"

# Watchlist Model for Movies
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, related_name='watchlist')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Watchlist of {self.user}"

# Readlist Model for Books
class Readlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, related_name='readlist')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Readlist of {self.user}"


class Profile(models.Model):
    MBTI_CHOICES = [
        ('INTJ', 'INTJ'), ('INTP', 'INTP'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mbti_type = models.CharField(max_length=4, choices=MBTI_CHOICES)

    def __str__(self):
        return self.user.username

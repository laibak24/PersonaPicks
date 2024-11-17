from django.db import models
from django.contrib.auth.models import AbstractUser

# MBTI Type Model
class MBTIType(models.Model):
    MBTI_CHOICES = [
        ('INTJ', 'INTJ'), ('INTP', 'INTP'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP')
    ]

    mbti_type_id = models.AutoField(primary_key=True)
    mbti_type = models.CharField(max_length=4, choices=MBTI_CHOICES, unique=True)

    def __str__(self):
        return self.mbti_type

# Custom User Model
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, default="Enter username")
    email = models.EmailField(unique=True, default="Enter email")
    mbti_type = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField(upload_to='avatars/', default="avatar.svg", null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
# Movie Model
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='media/movie_images/', default='default_movie.jpg')

    # Adding MBTI preferences
    first_preference = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True, related_name='preferred_movies_first')
    second_preference = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True, related_name='preferred_movies_second')
    third_preference = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True, related_name='preferred_movies_third')

    def __str__(self):
        return self.title

# Book Model
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    publication_year = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='book_images/', default='default_book.jpg')

    # Adding MBTI preferences
    first_preference = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True, related_name='preferred_books_first')
    second_preference = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True, related_name='preferred_books_second')
    third_preference = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True, related_name='preferred_books_third')

    def __str__(self):
        return self.title

# Song Model
class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    album = models.CharField(max_length=255, blank=True)
    release_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='song_images/', default='default_song.jpg')

    # Adding MBTI preferences
    first_preference = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True, related_name='preferred_songs_first')
    second_preference = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True, related_name='preferred_songs_second')
    third_preference = models.ForeignKey(MBTIType, on_delete=models.SET_NULL, null=True, related_name='preferred_songs_third')

    def __str__(self):
        return self.title

# Feedback Model
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    feedback_giver = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.feedback_giver}"

# Recommendations Model
class Recommendation(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    recommendation_for_user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True)
    recommended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.recommendation_for_user}"

STATUS_CHOICES = [
    ('not_started', 'Not Started'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]

# Watchlist Model for Movies
class Watchlist(models.Model):
    watchlist_user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, related_name='watchlist')
    added_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return f"Watchlist of {self.watchlist_user}"

# Readlist Model for Books
class Readlist(models.Model):
    readlist_user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, related_name='readlist')
    added_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    def __str__(self):
        return f"Readlist of {self.readlist_user}"

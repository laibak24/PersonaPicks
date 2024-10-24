from django.contrib import admin
from .models import MBTIType, User, Movie, Book, Song, Feedback, Recommendation, Watchlist, Readlist

admin.site.register(MBTIType)
admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Book)
admin.site.register(Song)
admin.site.register(Feedback)
admin.site.register(Recommendation)
admin.site.register(Watchlist)
admin.site.register(Readlist)

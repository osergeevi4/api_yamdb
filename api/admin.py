from django.contrib import admin
from .models import Title, Category, Review, Comments
from users.models import User

admin.site.register(User)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comments)

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create, name="create"),
    # if you see an int after /product(main urls.py) then assign it to product_id
    path('<int:product_id>', views.detail, name='detail'),
    path('<int:product_id>/upvote', views.upvote, name='upvote'),
]
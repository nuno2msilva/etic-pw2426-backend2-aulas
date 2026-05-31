from django.urls import path

from myapp import views

urlpatterns = [
    path("items/", views.item_list, name="item-list"),
    path("posts/", views.blogpost_list, name="blogpost-list"),
]

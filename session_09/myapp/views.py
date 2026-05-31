from django.http import JsonResponse

from .models import BlogPost, Item


def item_list(request):
    items = list(Item.objects.values("id", "name", "value"))
    return JsonResponse({"count": len(items), "results": items})


def blogpost_list(request):
    posts = list(BlogPost.objects.values("id", "title", "published_date"))
    for post in posts:
        post["published_date"] = str(post["published_date"])
    return JsonResponse({"count": len(posts), "results": posts})

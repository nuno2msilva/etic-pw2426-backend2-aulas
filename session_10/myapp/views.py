from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import CommentForm, RegisterForm
from .models import Comment


def home(request):
    comments = Comment.objects.select_related("user").order_by("-created_at")
    form = CommentForm()
    return render(request, "home.html", {"comments": comments, "form": form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    error = None
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", ""),
            password=request.POST.get("password", ""),
        )
        if user:
            login(request, user)
            return redirect("home")
        error = "Invalid username or password."
    return render(request, "login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
@require_http_methods(["POST"])
def submit_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        Comment.objects.create(user=request.user, content=form.cleaned_data["comment"])
    return redirect("home")

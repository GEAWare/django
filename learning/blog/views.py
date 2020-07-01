from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import RegistationForm, PostCreationForm
from .models import PostModel


def index(request):
    user = None
    posts = None
    paginate_by = 2
    try:
        pk = int(request.GET.get("page"))
    except:
        pk = 1
    context = {}
    if request.user.is_authenticated:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user:
            try:
                posts = user.postmodel_set.all()
            except:
                pass
        paginator = Paginator(posts, paginate_by).get_page(pk)
        range_ = [pk+i for i in [-3, -2, -1, 1, 2, 3]]
        range_.append(pk)
        c_pages = [page for page in range_ if page in Paginator(posts, paginate_by).page_range]
        context = {
            "page": paginator,
            "c_page": pk,
            "f_page": 1,
            "l_page": Paginator(posts, paginate_by).page_range[-1],
            "p_page": paginator.number - 1,
            "n_page": paginator.number + 1,
            "c_pages": sorted(c_pages),
        }

    return render(request, 'blog/index.html', context)


def new_post(request):
    if not request.user.id:
        return redirect("index")

    if request.method == "POST":
        data = request.POST.dict()
        data["author"] = request.user
        form = PostCreationForm(data, request.FILES)
        if form.is_valid():
            form.save()

    return render(request, 'blog/share_post.html')


def post_edit(request):
    if not request.user.id:
        return redirect("index")

    if request.method == "POST":
        post_id = request.POST["post_id"]
        post_model = PostModel.objects.get(id=post_id)
        context = {
            "post_model": post_model,
        }

        return render(request, 'blog/post.html', context)

    return redirect("index")


def post_save(request):
    if not request.user.id:
        return redirect("index")

    if request.method == "POST":
        post_id = request.POST["post_id"]
        new_title = request.POST["title"]
        new_content = request.POST["content"]
        post_model = PostModel.objects.get(id=post_id)
        post_model.title = new_title
        post_model.content = new_content
        try:
            new_image = request.FILES["image"]
            post_model.image = new_image
        except:
            pass
        post_model.save()

    return redirect("index")


def post_delete(request):
    if not request.user.id:
        return redirect("index")

    if request.method == "POST":
        post_id = request.POST["post_id"]
        post_model = PostModel.objects.get(id=post_id)
        post_model.delete()

    return redirect("index")


def account(request):
    if not request.user.id:
        return redirect("index")
    context = {
        "username": request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "posts_count": request.user.postmodel_set.count,
    }

    return render(request, "blog/account.html", context)


def registration(request):
    if request.method == "POST":
        form = RegistationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            if user:
                login(request, user)

    return redirect("index")


def login_(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user:
            login(request, user)

    return redirect("index")


def logout_(request):
    logout(request)
    return redirect("index")
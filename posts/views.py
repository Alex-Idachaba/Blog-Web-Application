from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Author, PostView
from subscribe.models import Subscribe
from .forms import PostForm, CommentForm
from django.urls import reverse
from django.views.generic import DeleteView

def about(request):
    context = {}
    return render(request, 'about.html', context)

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).distinct()
    context = {
        'queryset':queryset
    }
    return render(request, 'search_results.html', context)

def get_category_count():
    queryset = Post.objects.values(
        'categories__title').annotate(
        Count('categories__title'))
    return queryset

def home(request):
    category_count = get_category_count()
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    breaking =Post.objects.filter(breaking=True)

    paginator = Paginator(featured, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var) 
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        email = request.POST['email']
        new_subscription = Subscribe()
        new_subscription.email = email
        new_subscription.save()
        
    context = {
        'category_count': category_count,
        'object_list': featured,
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'latest': latest,
        'breaking': breaking,
    }
    return render(request, 'home.html', context)

def post_detail(request, id):
    category_count = get_category_count()
    latest = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'post': post,
        'latest': latest,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'post.html', context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None, 
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('home'))

# class PostDeleteView(DeleteView):
#     model = Post
#     template_name = 'post_delete.html'
#     success_url = 'home'

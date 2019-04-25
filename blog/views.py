from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from search.models import searchbox
from search.forms import SearchField
from django.core.paginator import Paginator

# def listing(request):
#     contact_list = Contacts.objects.all()
#     paginator = Paginator(posts, 10) # Show 25 contacts per page

#     page = request.GET.get('page')
#     contacts = paginator.get_page(page)
#     return render(request, 'list.html', {'contacts': contacts})



# var = User.objects.get(username = request.user)
#             posts = Post.objects.filter(author = var).order_by('-published_date')
#             se = SearchField()
#             return render(request, 'blog/post_list.html', {'posts': posts, 'search': se})











@login_required
def post_list(request):
    if request.method == "POST":
        se = SearchField(request.POST)
        if se.is_valid():
            b = False
            name = se.save(commit = False)
            x = name.text
            l = User.objects.values_list('username', flat=True)
            l = list(l)

            if x in l:
                b = True

            print(b)

            if b:
                m = User.objects.get(username = x)
                d = Post.objects.filter(author = m).order_by('-published_date')

            # paginator1 = Paginator(d, 6)
            # page1 = request.GET.get('page1')
            # post_list1 = paginator1.get_page(page1)

            return render(request, 'blog/another_profile.html', {'d':d, 'search': se, 'bool': b, 'text':x, 'email':m.email, 'img_url':m.profile.p_image.url})

            if not b:
                return render(request, 'blog/another_profile.html', {'search': se, 'bool': b, 'text':x})

    else:
        if request.user.is_authenticated:
            var = User.objects.get(username = request.user)
            posts = Post.objects.filter(author = var).order_by('-published_date')
            se = SearchField()
            paginator = Paginator(posts, 6)
            page = request.GET.get('page')
            post_list = paginator.get_page(page)
            return render(request, 'blog/post_list.html', {'posts':post_list , 'search': se})

        elif request.user.is_authenticated is False:
            return render(request, 'blog/post_list.html', {})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        flag = 1
    else:
        flag = None
    return render(request, 'blog/post_detail.html', {'post': post, 'flag': flag})

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def go(request, pk):
    remove = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/yousure.html', {'remove':remove})
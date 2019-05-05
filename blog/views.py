from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from search.models import searchbox
from search.forms import SearchField
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from comments.models import comments
from comments.forms import comment_form

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


    init_data  ={
        "content_type":post.get_content_type(),
        "object_id":post.id
    }

    form = comment_form(request.POST or None, initial = init_data)

    if form.is_valid():
        print(form.cleaned_data)
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model = c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = comments.objects.filter(id = parent_id)

            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj = parent_qs.first()


        new_comment, created = comments.objects.get_or_create(
                                        user = request.user,
                                        content_type = content_type,
                                        object_id = obj_id,
                                        content = content_data,
                                        parent = parent_obj,
                                )
        
        return redirect('post_detail', pk=post.pk)


        # return HttpResponseRedirect(new_comment.content_object.get_absolute_url)








    # content_type = ContentType.objects.get_for_model(Post)
    # obj_id = post.id
    # r = comments.objects.filter_by_instance(post)
    r = post.comments()
    # print(obj_id,'  ', content_type)
    return render(request, 'blog/post_detail.html', {'post': post, 'flag': flag, 'comments':r, 'form':form})

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
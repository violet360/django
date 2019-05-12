from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
# from .models import Post
# from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from search.models import searchbox
from search.forms import SearchField
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from comments.models import comments
from comments.forms import comment_form
from messaging.models import message
from .forms import msg_form
from itertools import chain
from operator import attrgetter


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





def msg_view(request, var):
	m1 = User.objects.get(pk = var)
	m2 = User.objects.get(username = request.user)
	obj1 = message.objects.filter(sender = m2, receiver = m1)
	obj2 = message.objects.filter(receiver = m2, sender = m1)
	result_list = sorted(chain(obj1, obj2),key=attrgetter('timestamp'))
	if request.method == 'POST':
		form = msg_form(request.POST)
		if form.is_valid():
			f = form.save(commit = False)
			# f.sender = m2 
			# f.receiver = m1
			new_msg = message.objects.create(sender = m2, receiver = m1, text = f.text)
			# f.save()
			return redirect('msg_view', var = m1.pk)

#things in data base can also be saved by eliminating line 46 and uncommenting line 44, 45, 47, 


	for msg in result_list:
		print(type(msg.sender.username),'   ',type(m1.username),'   ',type(msg.receiver.username))

	else:
		form = msg_form()
		
	return render(request, 'messages/msg_view.html', {'conversation':result_list, 'form':form, 'A':request.user.username, 'B':m1.username})



def msg_list(request):
	sent_list = []
	received_list = []
	sent = message.objects.filter(sender = request.user)
	received = message.objects.filter(receiver = request.user)
	for x in sent:
		if x.receiver.username not in sent_list:
			sent_list.append(x.receiver)

	for y in received:
		if y.sender.username not in received_list:
			received_list.append(y.sender)

	print(received_list,'    ', sent_list)

	final_list = list(set(received_list) | set(sent_list)) 

	print(request.path_info)

	return render(request, 'messages/msg_list.html', {'msgs':final_list})




from django.shortcuts import render, get_object_or_404, redirect
from .models import comments
from .forms import comment_form
from django.contrib.contenttypes.models import ContentType



def com_list(request, x):

	obj = comments.objects.get(id = x)
	content_object = obj.content_object
	content_id = obj.content_object.id

	init_data  ={
        "content_type":obj.content_type,
        "object_id":obj.object_id
    }

	form = comment_form(request.POST or None,initial = init_data)
	  


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
        
		return redirect('com_list', x=obj.id)

	return render(request, "com_list.html", {"c":obj, "form":form})
# Create your views here.

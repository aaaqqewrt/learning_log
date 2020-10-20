from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from .models import Topic,Entry,ReadNum
from comment.models import Comment
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .forms import TopicForm,EntryForm
from django.conf import settings
from read_statistics.utils import read_statistics_once_read
from comment.forms import CommentForm

def index(request):
	return render(request, 'index.html')

#def get_entry_list_common_data(request,entries_all_list)

# ~ @login_required
def topics(request):
	entries=Entry.objects.all()
	for entry in entries:
		#user=entry.topic.owner
		topic=entry.topic
	paginator=Paginator(entries,settings.ENTRIES_EACHPAGE_NUM)
	page_num=request.GET.get('page',1)#获取url页码参数（GET请求）
	page_of_entries=paginator.get_page(page_num)
	current_page_num=page_of_entries.number
	#获取当前页码，前后各两页的页码范围
	page_range = list(range(max(current_page_num - 2, 1), current_page_num))+ \
				list(range(current_page_num, min(current_page_num + 2, paginator.num_pages + 1)))
	
	#加上省略页码标记
	if page_range[0] - 1 >=2:
		page_range.insert(0,'...')
	if paginator.num_pages - page_range[-1] >=2:
		page_range.append('...')
	
	#加上首页和尾页
	if page_range[0] !=1:
		page_range.insert(0,1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)
	
	topics=Topic.objects.all()
	topic_list=[]
	for topic in topics:
		topic.entry_count=Entry.objects.filter(topic=topic).count()
		topic_list.append(topic)
	
	entry_dates=Entry.objects.dates('created_date','month',order="DESC")
	entry_dates_dict={}
	for entry_date in entry_dates:
		entry_count=Entry.objects.filter(created_date__year=entry_date.year,
										created_date__month=entry_date.month).count()
		entry_dates_dict[entry_date]=entry_count
		
	context={}
	context['topics']=topic_list
	context['user']=request.user
	# ~ context['topic']=topic
	context['entries']=page_of_entries.object_list
	context['page_of_entries']=page_of_entries
	context['page_range']=page_range
	context['entry_dates']=entry_dates_dict
#	context['topics']=Topic.objects.filter(owner=request.user).order_by('date_added')
	return render(request,'learning_logs/topics.html',context)

# ~ @login_required
def topic(request,topic_id):

	topic=get_object_or_404(Topic, id=topic_id)
	entries=Entry.objects.filter(topic_id=topic_id)
	paginator=Paginator(entries,settings.ENTRIES_EACHPAGE_NUM)
	page_num=request.GET.get('page',1)#获取url页码参数（GET请求）
	page_of_entries=paginator.get_page(page_num)
	current_page_num=page_of_entries.number
	#获取当前页码，前后各两页的页码范围
	page_range = list(range(max(current_page_num - 2, 1), current_page_num))+ \
				list(range(current_page_num, min(current_page_num + 2, paginator.num_pages + 1)))
	
	#加上省略页码标记
	if page_range[0] - 1 >=2:
		page_range.insert(0,'...')
	if paginator.num_pages - page_range[-1] >=2:
		page_range.append('...')
	
	#加上首页和尾页
	if page_range[0] !=1:
		page_range.insert(0,1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)
	
	topics=Topic.objects.all()
	topic_list=[]
	for topic in topics:
		topic.entry_count=Entry.objects.filter(topic=topic).count()
		topic_list.append(topic)
	
	entry_dates=Entry.objects.dates('created_date','month',order="DESC")
	entry_dates_dict={}
	for entry_date in entry_dates:
		entry_count=Entry.objects.filter(created_date__year=entry_date.year,
										created_date__month=entry_date.month).count()
		entry_dates_dict[entry_date]=entry_count	
	
	context={}
	context['topic']=topic
	context['entries']=page_of_entries.object_list
	context['page_of_entries']=page_of_entries
	context['page_range']=page_range
	context['entry_dates']=entry_dates_dict
	context['topics']=topic_list
	#context['topics']=Topic.objects.all()

	return render(request, 'learning_logs/topic.html',context)

@login_required
def new_topic(request):
	if request.method != 'POST':
		form=TopicForm()
	else:
		form=TopicForm(request.POST)
		if form.is_valid():
			new_topic=form.save(commit=False)
			new_topic.owner=request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))
	context={'form':form}
	return render(request,'learning_logs/new_topic.html',context)

# ~ @login_required	
def show_entry(request,entry_id):
	entry=get_object_or_404(Entry,id=entry_id)
	topic=entry.topic
	read_cookie_key=read_statistics_once_read(request,entry)
	
	entry_content_type=ContentType.objects.get_for_model(entry)	
	comments=Comment.objects.filter(content_type=entry_content_type, object_id=entry.id, parent=None)
	
	context={}
	context['previous_entry']=Entry.objects.filter(created_date__gt=entry.created_date).last()
	context['next_entry']=Entry.objects.filter(created_date__lt=entry.created_date).first()
	context['topic']=topic
	context['entry']=entry
	context['comments']=comments.order_by('-comment_time')
	context['comment_form']=CommentForm(initial={'content_type':entry_content_type.model,'object_id':entry_id,'reply_comment_id':0})
	response = render(request,'learning_logs/show_entry.html',context)
	response.set_cookie(read_cookie_key, 'true')
	return response

@login_required			
def new_entry(request,topic_id):
	topic=Topic.objects.get(id=topic_id)
	if request.method!='POST':
		form=EntryForm()
	else:
		form=EntryForm(data=request.POST)
		if form.is_valid():
			new_entry=form.save(commit=False)
			new_entry.topic=topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',
												args=[topic_id]))
	context={'form':form, 'topic':topic}
	return render(request,'learning_logs/new_entry.html',context)

@login_required			
def edit_entry(request,entry_id):
	entry=Entry.objects.get(id=entry_id)
	topic=entry.topic
	if topic.owner!=request.user:
		raise Http404
	if request.method!='POST':
		form=EntryForm(instance=entry)
	else:
		form=EntryForm(instance=entry,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',
												args=[topic.id]))
	context={'entry':entry,'topic':topic,'form':form}
	return render(request,'learning_logs/edit_entry.html',context)


@login_required
def del_entry(request,entry_id):
	entry=Entry.objects.get(id=entry_id)
	topic=entry.topic
	if topic.owner!=request.user:
		raise Http404
	if request.method !='POST':
		form=EntryForm(instance=entry)
	else:
		return entry.remove()
	context={'topic':topic,'entry':entry,'form':form}
	return render(request,'learning_logs/del_entry.html',context)
			
def entry_date(request,year,month):
	entries=Entry.objects.filter(created_date__year=year, created_date__month=month)
	for entry in entries:
		user=entry.topic.owner
		topic=entry.topic
	paginator=Paginator(entries,settings.ENTRIES_EACHPAGE_NUM)
	page_num=request.GET.get('page',1)#获取url页码参数（GET请求）
	page_of_entries=paginator.get_page(page_num)
	current_page_num=page_of_entries.number
	#获取当前页码，前后各两页的页码范围
	page_range = list(range(max(current_page_num - 2, 1), current_page_num))+ \
				list(range(current_page_num, min(current_page_num + 2, paginator.num_pages + 1)))
	
	#加上省略页码标记
	if page_range[0] - 1 >=2:
		page_range.insert(0,'...')
	if paginator.num_pages - page_range[-1] >=2:
		page_range.append('...')
	
	#加上首页和尾页
	if page_range[0] !=1:
		page_range.insert(0,1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)
	
	topics=Topic.objects.all()
	topic_list=[]
	for topic in topics:
		topic.entry_count=Entry.objects.filter(topic=topic).count()
		topic_list.append(topic)
		
	context={}
	context['entry_date']= '%s年%s月' % (year,month)
	context['entries']=page_of_entries.object_list
	context['topic']=topic
	context['page_of_entries']=page_of_entries
	context['page_range']=page_range
	context['topics']=topic_list
	context['entry_dates']=Entry.objects.dates('created_date','month',order="DESC")
	return render(request, 'learning_logs/entry_date.html',context)




















	

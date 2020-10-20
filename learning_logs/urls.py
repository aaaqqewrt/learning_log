
from django.urls import path
from . import views

app_name='learning_logs'
urlpatterns = [
	path('',views.index, name='index'),
	path('topics/', views.topics, name='topics'),
	path("topics/(?<topic_id>\d+)/",views.topic,name='topic'),
	path('new_topic/',views.new_topic,name='new_topic'),
	path('show_entry/(?<entry_id>\d+)/',views.show_entry,name='show_entry'),
	path('new_entry/(?<topic_id>\d+)/',views.new_entry,name='new_entry'),
	path('edit_entry/(?<entry_id>\d+)/',views.edit_entry,name='edit_entry'),
	path('del_entry/(?<entry_id>\d+)/',views.del_entry,name='del_entry'),
	path('entry_date/<int:year>/<int:month>',views.entry_date,name='entry_date'),
]

from django.contrib import admin

# Register your models here.
from learning_logs.models import Topic, Entry

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_display=('id','text')

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
	list_display=('id','title','topic','get_read_num','created_date','published_date')


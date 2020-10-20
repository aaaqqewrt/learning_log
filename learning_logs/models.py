from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNum
from read_statistics.models import ReadNumExpandMethod

class Topic(models.Model):
	text=models.CharField(max_length=200)
	date_added=models.DateTimeField(auto_now_add=True)
	owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	
	def __str__(self):
		return self.text
		
class Entry(models.Model,ReadNumExpandMethod):
	topic=models.ForeignKey(Topic, on_delete=models.CASCADE)
	title=models.CharField(max_length=200,default="")
	text=RichTextUploadingField()
	created_date=models.DateTimeField(auto_now_add=True)
	published_date=models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name_plural='entries'
		ordering=['-created_date']
	
	def __str__(self):
		if self.text<str(50):
			return self.text[:50]
		else:
			return self.text[:50]+'...'













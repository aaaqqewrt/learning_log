from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings

class Comment(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	text=RichTextUploadingField()
	comment_time=models.DateTimeField(auto_now_add=True)
	user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="comments",on_delete=models.CASCADE)

	root = models.ForeignKey('self', related_name='root_comment',null=True,on_delete=models.CASCADE)
	parent=models.ForeignKey('self', related_name='parent_comment',null=True,on_delete=models.CASCADE)
	reply_to=models.ForeignKey(settings.AUTH_USER_MODEL,related_name="replies", null=True, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.text
	class META:
		ordering=['-comment_time']	

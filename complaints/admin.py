from django.contrib import admin 
from .models import Complaint, ComplaintCategory, ComplaintHistory 
admin.site.register(ComplaintCategory) 
admin.site.register(Complaint) 
admin.site.register(ComplaintHistory) 

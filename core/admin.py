from django.contrib import admin

# Register your models here.
from .models import Project, Task, Tag, ProjectMembership, SecurityLog
 
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(ProjectMembership)
admin.site.register(SecurityLog)

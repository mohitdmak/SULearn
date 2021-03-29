from django.contrib import admin
from .models import CreatorProfile, LearnerProfile, Courses, Modules, ClassroomModules, Reviews, Classroom, FollowList

admin.site.register(CreatorProfile)
admin.site.register(LearnerProfile)
admin.site.register(Courses)

admin.site.register(Modules)
admin.site.register(Reviews)
admin.site.register(FollowList)
admin.site.register(ClassroomModules)
admin.site.register(Classroom)
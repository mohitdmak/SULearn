from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as Homeviews

urlpatterns = [
    path('', Homeviews.home, name = 'home'),
    path('about/', Homeviews.about, name = 'about'),
    path('accounts/', include('allauth.urls')),
    path('register/', Homeviews.register, name = 'register'),
    path('learner-register/', Homeviews.LearnerRegisterHandler, name = 'learner-register'),
    path('creator-register/', Homeviews.CreatorRegisterHandler, name = 'creator-register'),
    path('profile/view/<int:pk>/', Homeviews.profile, name = 'seeprofile'),
    path('profile/follow/<int:pk>/', Homeviews.follow, name = 'follow'),
    path('profile/unfollow/<int:pk>/', Homeviews.unfollow, name = 'unfollow'),
    path('createcourse/', Homeviews.createcourse, name = 'create-course'),
    path('mycourses/', Homeviews.mycourses, name = 'mycourses'),
    path('modulecreation/', Homeviews.modulecreation, name = 'modulecreation'),
    path('createmodule/course/<int:pk>/', Homeviews.createmodule, name = 'create-module'),
    path('allcourses/', Homeviews.allcourses, name = 'allcourses'),
    path('course/details/<int:pk>/', Homeviews.showcourse, name = 'show-course'),
    path('course/enroll/<int:pk>', Homeviews.enroll, name = 'enroll'),
    path('course/study/<int:pk>/', Homeviews.studycourse, name = 'study'),
    path('course/module/<int:pk>/', Homeviews.studymodule, name = 'study-module'),
    path('course/module/complete/<int:pk>/', Homeviews.completemodule, name = 'complete-module'),
    path('course/rateandreveiw/<int:pk>/', Homeviews.rateandreview, name = 'rateandreview'),
    path('search/', Homeviews.searchbytag, name = 'search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
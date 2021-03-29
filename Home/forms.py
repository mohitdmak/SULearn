from django import forms
from django.db import models
from django.db.models import fields
from .models import CreatorProfile, LearnerProfile, Courses, Modules, Classroom, Reviews, FollowList, ClassroomModules

class CreatorRegisterForm(forms.Form):
    Name = forms.CharField(max_length = 200)
    Email = forms.EmailField(max_length = 200)
    Date_Of_Birth = forms.DateField()
    City = forms.CharField(max_length = 200)
    State = forms.CharField(max_length = 200)
    Educational_Qualification = forms.CharField(max_length = 200)
    

class LearnerRegisterForm(forms.Form):
    Name = forms.CharField(max_length = 200)
    Email = forms.EmailField(max_length = 200)
    Date_Of_Birth = forms.DateField()
    City = forms.CharField(max_length = 200)
    State = forms.CharField(max_length = 200)


class CourseCreationForm(forms.Form):
    Course_Name = forms.CharField(max_length = 200)
    Course_Description =  forms.CharField(widget = forms.Textarea)
    Course_Tag = forms.CharField(max_length = 200)

class ModuleCreationForm(forms.Form):
    Title = forms.CharField(max_length = 200)
    Content = forms.CharField(widget = forms.Textarea)
    link = forms.URLField()
    
class RateAndReviewForm(forms.Form):
    ratechoices = [(0,'0'), (1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')]
    RateCreator = forms.CharField(label = 'Rate the instructor out of 5 (On the Basis of the ease with you understood the concepts) : ', widget = forms.Select(choices = ratechoices))
    Rate = forms.CharField(label = 'Rate the course out of 5 (On the Basis of the structure and Quality of Content Presented): ', widget = forms.Select(choices = ratechoices))
    Review = forms.CharField(widget = forms.Textarea)

class SearchByTag(forms.Form):
    tag = forms.CharField(max_length = 200)
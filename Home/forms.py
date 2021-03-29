from django import forms
from django.db import models
from django.db.models import fields
from .models import CreatorProfile, LearnerProfile, Courses, Modules, Classroom, Reviews, FollowList, ClassroomModules

class CreatorRegisterForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = [
            'Name',
            'Email',
            'Date_Of_Birth',
            'City',
            'State',
            'Educational_Qualification'
        ]

class LearnerRegisterForm(forms.ModelForm):
    class Meta:
        model = LearnerProfile
        fields = [
            'Name',
            'Email',
            'Date_Of_Birth',
            'City',
            'State'
        ]


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = [
            'Course_Name',
            'Course_Desc',
            'Course_Tag'
        ]

class ModuleCreationForm(forms.ModelForm):
    class Meta:
        model = Modules
        fields = [
            'Title',
            'Content',
            'link'
        ]
    
class RateAndReviewForm(forms.Form):
    ratechoices = [(0,'0'), (1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5')]
    RateCreator = forms.CharField(label = 'Rate the instructor out of 5 (On the Basis of the ease with you understood the concepts) : ', widget = forms.Select(choices = ratechoices))
    Rate = forms.CharField(label = 'Rate the course out of 5 (On the Basis of the structure and Quality of Content Presented): ', widget = forms.Select(choices = ratechoices))
    Review = forms.CharField(widget = forms.Textarea)

class SearchByTag(forms.Form):
    tag = forms.CharField(max_length = 200)
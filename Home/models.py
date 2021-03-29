from django.db import models
from django.contrib.auth.models import User


class CreatorProfile(models.Model):
    creatorusr = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'creatorprofile')
    Name = models.CharField(max_length = 200)
    Email = models.EmailField(max_length = 200)
    Date_Of_Birth = models.DateField(default = None)
    City = models.CharField(max_length = 200)
    State = models.CharField(max_length = 200)
    Date_Of_Joining = models.DateField(auto_now = True)
    Educational_Qualification = models.CharField(max_length = 200)
    rating = models.FloatField(default = 3)

class LearnerProfile(models.Model):
    learnerusr = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'learnerprofile')
    Name = models.CharField(max_length = 200)
    Email = models.EmailField(max_length = 200)
    Date_Of_Birth = models.DateField(default = None)
    City = models.CharField(max_length = 200)
    State = models.CharField(max_length = 200)
    Date_Of_Joining = models.DateField(auto_now = True)

class FollowList(models.Model):
    usertofollow = models.ForeignKey(User,related_name='followed_by',on_delete=models.CASCADE)
    followings = models.ManyToManyField(User,related_name='followings')
    def __str__(self):
        return str(self.usertofollow)

class Courses(models.Model):
    Course_Name = models.CharField(max_length = 200)
    Course_Desc = models.TextField()
    Creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'createdcourses')
    Course_Tag = models.CharField(max_length = 200)
    rating = models.FloatField(default = 3)

class Modules(models.Model):
    Title = models.CharField(max_length = 200)
    Content = models.TextField()
    index = models.IntegerField(default = 1)
    Course = models.ForeignKey(Courses, on_delete = models.CASCADE, related_name = 'allmodules')
    link = models.URLField()

class Classroom(models.Model):
    learners = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'classes')
    courses = models.ForeignKey(Courses, on_delete = models.CASCADE, related_name = 'classrooms')
    Course_completed = models.BooleanField(default = False)

class ClassroomModules(models.Model):
    learners = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'classesmodules')
    modules = models.ForeignKey(Modules, on_delete = models.CASCADE, related_name = 'classrooms')
    completed = models.BooleanField(default = False)

class Reviews(models.Model):
    rating = models.FloatField(default = 3)
    course = models.ForeignKey(Courses, on_delete = models.CASCADE, related_name = 'reviews')

class ReviewsCreator(models.Model):
    rating = models.FloatField(default = 3)
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'creatorrating')

class Testimony(models.Model):
    testimony = models.TextField()
    course = models.ForeignKey(Courses, on_delete = models.CASCADE, related_name = 'testimonies')
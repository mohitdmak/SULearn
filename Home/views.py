from django.shortcuts import render, redirect
from .forms import CreatorRegisterForm, LearnerRegisterForm, CourseCreationForm, ModuleCreationForm, RateAndReviewForm, SearchByTag
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CreatorProfile, LearnerProfile, FollowList, Courses, Modules, ClassroomModules, Classroom, Reviews, ReviewsCreator, Testimony
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

#send_mail('Welcome to the BITS Community Page','We are glad that you have joined our community. Try to answer any questions that users may post here, and also clear your doubts. \nThis was just an automated test mail to check if you can recieve announcements via mail in future. You can confirm it by replying to this email. \nLOL.\n\n <author> mohitdmak','settings.EMAIL_HOST_USER',list,fail_silently=False)

def home(request):
    return render(request, 'Home/home.html')

def about(request):
    return render(request, 'Home/about.html')

def register(request):
    if(CreatorProfile.objects.filter(creatorusr = request.user).exists() or LearnerProfile.objects.filter(learnerusr = request.user).exists()):
        messages.success(request, 'Welcome Back !')
        return redirect('home')
    messages.success(request, 'Choose one path below and Register ! ')
    list = [request.user.email]
    send_mail('Welcome to Coursera - Lite !','We are glad that you have joined our community.\n Make Sure to choose a path out of Creator/Learner and complete your profile in order to use the site further.\n This was just an automated test mail to check if you can recieve announcements via mail in future. You can confirm it by replying to this email.\n\n <author> mohitdmak','settings.EMAIL_HOST_USER',list,fail_silently=False)

    return render(request, 'Home/register.html')

def CreatorRegisterHandler(request):
    if request.method == 'POST':
        user_form=CreatorRegisterForm(request.POST)

        if user_form.is_valid():
            user_form.instance.creatorusr = request.user
            user_form.save()
            username = user_form.cleaned_data.get('Name')
            messages.success(request,f'CONGRATS {username} !, Your Creator profile is now created!')
            return redirect("home")
    else:
        user_form = CreatorRegisterForm()
        context={'user_form':user_form}
        messages.success(request,f'Please complete the verification below !')
        return render(request, 'Home/Creator_Register.html', context)


def LearnerRegisterHandler(request):
    if request.method == 'POST':
        user_form = LearnerRegisterForm(request.POST)

        if user_form.is_valid():
            user_form.instance.learnerusr = request.user
            user_form.save()
            username = user_form.cleaned_data.get('Name')
            messages.success(request,f'CONGRATS {username} !, Your Learner profile is now created!')
            return redirect("home")
    else:
        user_form = LearnerRegisterForm()
        context={'user_form':user_form}
        messages.success(request,f'Please complete the verification below !')
        return render(request, 'Home/Learner_Register.html', context)

def profile(request, **kwargs):
    if User.objects.filter(id = kwargs['pk']).exists():
        usr = User.objects.filter(id = kwargs['pk'])[0]
        if CreatorProfile.objects.filter(creatorusr = usr).exists():
            pic = usr.socialaccount_set.all()[0].extra_data['picture']
            if request.user.is_authenticated:
                if(FollowList.objects.filter(followings = request.user, usertofollow = usr).exists()):
                    foll = 'u'
                else:
                    foll = 'f'
                return render(request, 'Home/cprofile.html', {'profile': usr.creatorprofile, 'foll': foll, 'pic': pic})
            return render(request, 'Home/cprofile.html', {'profile': usr.creatorprofile, 'pic': pic})
        else:
            pic = usr.socialaccount_set.all()[0].extra_data['picture']
            return render(request, 'Home/lprofile.html', {'profile' : usr.learnerprofile, 'pic': pic})
    else:
        messages.success(request,f'The requested User profile does not exist :(')
        return redirect('home')

@login_required(redirect_field_name = 'register')
def follow(request, **kwargs):
    usr = User.objects.filter(id = kwargs['pk'])[0]
    request.user.followings.create(usertofollow = usr)
    messages.success(request, f'You are now following {usr.creatorprofile.Name} !')
    return redirect('seeprofile', pk = usr.id)

def unfollow(request, **kwargs):
    usr = User.objects.filter(id = kwargs['pk'])[0]
    todelete = request.user.followings.filter(usertofollow = usr)
    todelete.delete()
    request.user.save()
    messages.success(request, f'You are now unfollowing {usr.creatorprofile.Name} !')
    return redirect('seeprofile', pk = usr.id)


@login_required(redirect_field_name = 'register')
def createcourse(request):
    if CreatorProfile.objects.filter(creatorusr = request.user).exists():
        if(request.method == 'POST'):
            course_form = CourseCreationForm(request.POST)

            if course_form.is_valid():
                course_form.instance.Creator = request.user
                course_form.save()
                messages.success(request, 'Congrats! Your Course is now Published !')

                list = []
                for learners in request.user.followed_by.all():
                    list.append(learners.followings.all()[0].email)
                send_mail(f'Creator {request.user.creatorprofile.Name} has created a New Course !',f'You recieved this mail because you follow the Creator : {request.user.creatorprofile.Name}.\n You can unsubscribe by unfollowing the creator. \n\n <author> mohitdmak','settings.EMAIL_HOST_USER',list,fail_silently=False)

                return redirect('modulecreation')

        else:
            course_form = CourseCreationForm()
            return render(request, 'Home/CreateCourse.html', {'course_form': course_form})
    else:
        messages.success(request, 'Sorry, you must be a verified Creator to Launch a Course.')
        return redirect('home')

@login_required(redirect_field_name = 'register')
def modulecreation(request):
    if CreatorProfile.objects.filter(creatorusr = request.user).exists():
        messages.success(request, 'Choose a course to add a module to !')
        return redirect('mycourses')
    else:
        messages.success(request, 'Sorry, you must be a verified Creator to Create a Modulee.')
        return redirect('home')

@login_required(redirect_field_name = 'register')
def mycourses(request):
    if CreatorProfile.objects.filter(creatorusr = request.user).exists():
        return render(request, 'Home/mycourses.html', {'courses': CreatorProfile.objects.filter(creatorusr = request.user)[0].creatorusr.createdcourses.all()})
    else:
        return render(request, 'Home/mycourse2.html', {'courses': LearnerProfile.objects.filter(learnerusr = request.user)[0].learnerusr.classes.all(), 'usr':request.user})


@login_required(redirect_field_name = 'register')
def createmodule(request, **kwargs):
    if CreatorProfile.objects.filter(creatorusr = request.user).exists():
        if(request.method == 'POST'):
            module_form = ModuleCreationForm(request.POST)
            if module_form.is_valid():
                modulecourse = Courses.objects.filter(id = kwargs['pk'])[0]

                if modulecourse.Creator == request.user:
                    moduleno = modulecourse.allmodules.count() + 1
                    module_form.instance.Course = modulecourse
                    module_form.instance.index = moduleno
                    module_form.save()
                    messages.success(request, f'Congrats! You have added modules to course {modulecourse.Course_Name} !')
                    return redirect('mycourses')
                else:
                    messages.success(request, 'You do not have access rights to this course !')
                    return redirect('modulecreation')
        else:
            module_form = ModuleCreationForm()
            return render(request, 'Home/CreateModule.html', {'module_form': module_form})

    else:
        messages.success(request, 'You must be a verified Creator to add modules !')
        return redirect('home')

def allcourses(request):
    return render(request, 'Home/allcourses.html', {'courses': Courses.objects.all()})

def showcourse(request, **kwargs):
    coursetoshow = Courses.objects.filter(id = kwargs['pk'])[0]
    pic = coursetoshow.Creator.socialaccount_set.all()[0].extra_data['picture']
    if request.user.is_authenticated and Classroom.objects.filter(learners = request.user, courses = coursetoshow).exists():
        next = 'view'
    else:
        next = 'enroll'
    return render(request, 'Home/ShowCourse.html', {'course': coursetoshow, 'pic': pic, 'next': next})


def enroll(request, **kwargs):
    coursetoenroll = Courses.objects.filter(id = kwargs['pk'])[0]
    if LearnerProfile.objects.filter(learnerusr = request.user).exists():
        Classroom.objects.create(learners = request.user, courses = coursetoenroll)
        for module in coursetoenroll.allmodules.all():
            ClassroomModules.objects.create(learners = request.user, modules = module)
        messages.success(request, 'Congrats! You have enrolled for the course!')
        return redirect('study', pk = coursetoenroll.id)
    else:
        messages.success(request, 'Being a Creator, You cannot Study Courses !')
        return redirect('home')

@login_required(redirect_field_name = 'register')
def studycourse(request, **kwargs):
    if LearnerProfile.objects.filter(learnerusr = request.user).exists():
        currentcourse = Courses.objects.filter(id = kwargs['pk'])[0]
        if Classroom.objects.filter(learners = request.user, courses = currentcourse).exists():

            mainclass = Classroom.objects.filter(learners = request.user, courses = currentcourse)[0]
            if mainclass.Course_completed == True:
                check = True
            else:
                check = False

            return render(request, 'Home/StudyCourse.html', {'course': currentcourse, 'check': check})
        else:
            messages.success(request, 'You need to first enroll for the course!')
            return redirect('show-course', pk = currentcourse.id)
    else:
        messages.success(request, 'Being a Creator, You cannot Study Courses !')
        return redirect('home')

@login_required(redirect_field_name = 'register')
def studymodule(request, **kwargs):
    if LearnerProfile.objects.filter(learnerusr = request.user).exists():
        currentmodule = Modules.objects.filter(id = kwargs['pk'])[0]
        if Classroom.objects.filter(learners = request.user, courses = currentmodule.Course).exists():
            classroom = ClassroomModules.objects.filter(learners = request.user, modules = currentmodule)[0]
            if classroom.completed:
                check = 'complete'
            else:
                check = 'notcomplete'
            return render(request, 'Home/StudyModule.html', {'module': currentmodule, 'check' : check})
        else:
            messages.success(request, 'You must first enroll for the course !')
            return redirect('show-course', pk = currentmodule.Course.id)
    else:
        messages.success(request, 'Being a Creator, You cannot Study Courses !')
        return redirect('home')

def completemodule(request, **kwargs):
    moduletocomplete = Modules.objects.filter(id = kwargs['pk'])[0]
    classroom = ClassroomModules.objects.filter(learners = request.user, modules = moduletocomplete)[0]
    classroom.completed = True
    classroom.save()
    messages.success(request, 'Congrats! You have Studied the module !')

    number = 0
    for module in moduletocomplete.Course.allmodules.all():
        check = ClassroomModules.objects.filter(learners = request.user, modules = module)[0]
        if check.completed:
            number += 1

    if number == moduletocomplete.Course.allmodules.count():
        messages.success(request, 'Congrats! You have also Completed the Course !!!')
        mainclass = Classroom.objects.filter(learners = request.user, courses = moduletocomplete.Course)[0]
        mainclass.Course_completed = True
        mainclass.save()

        return redirect('rateandreview', pk = moduletocomplete.Course.id)

    return redirect('study', pk = moduletocomplete.Course.id)

def rateandreview(request, **kwargs):
    course = Courses.objects.filter(id = kwargs['pk'])[0]
    if request.method == 'POST':
        rate_form = RateAndReviewForm(request.POST)
        if rate_form.is_valid():
            creator = course.Creator

            rated = int(rate_form.cleaned_data.get('Rate'))
            Reviews.objects.create(rating = rated, course = course)
            ratedcreator = int(rate_form.cleaned_data.get('RateCreator'))
            ReviewsCreator.objects.create(rating = ratedcreator, creator = creator)

            Review = rate_form.cleaned_data.get('Review')

            total = course.reviews.count()
            totalcreator = creator.creatorrating.count()

            new = 0
            newcreator = 0

            for x in course.reviews.all():
                new += x.rating
            for y in creator.creatorrating.all():
                newcreator += y.rating

            course.rating = new/total
            course.testimonies.create(testimony = Review)
            course.save()

            creator.creatorprofile.rating = newcreator/totalcreator
            creator.creatorprofile.save()

            messages.success(request, 'Thanks for providing your valuable feedback')
            return redirect('home')
    else:
        rate_form = RateAndReviewForm
        return render(request, 'Home/RateAndReview.html', {'rate_form': rate_form})


def searchbytag(request):
    if request.method == 'POST':
        search_form = SearchByTag(request.POST)

        if search_form.is_valid():
            tag = search_form.cleaned_data.get('tag')
            return render(request, 'Home/searched.html', {'courses': Courses.objects.filter(Course_Tag__icontains = tag)})

    else:
        search_form = SearchByTag
        totaltags = []
        for course in Courses.objects.all():
            totaltags.append(course.Course_Tag)

        searchedtags = set(totaltags)
        return render(request, 'Home/searchbytag.html', {'search_form': search_form, 'tags': searchedtags})
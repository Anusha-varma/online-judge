from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from problems.models import CodeSubmission,Problem, Contest
from django.contrib.auth import authenticate, login
from .forms import CodeSubmissionForm
from django.db.models import Max, F,Sum
from django.utils import timezone
from django.contrib import messages
from django.utils.timezone import localtime
# Create your views here.
def HomePage(request):
    last_contest = Contest.objects.filter(end_time__lt=timezone.now()).order_by('-end_time').first()
    leaderboard = []
    top_users = (
        CodeSubmission.objects.values('user__username')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')[:5]
    )
    if last_contest:
        leaderboard = (
            CodeSubmission.objects.filter(problem__contest=last_contest)
            .values('user__username')
            .annotate(total_score=Sum('score'))
            .order_by('-total_score')[:5]  # Top 5
        )
    context={
      "top_users": top_users,
        "show": request.GET.get('show', 'login')  ,
        "last_contest":last_contest
    }
    return render(request, "Home.html", context)

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,'Login Successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('/?show=login')
    
    return render(request, 'Login.html')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('/?show=login')
        else:
            return render(request, 'Home.html', {
                'form': form,
                'show': 'register'
            })
    else:
        form = UserCreationForm()
    return render(request, 'Register.html', {'form': form})
@login_required
def home(request):
    user_submissions = CodeSubmission.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "Home.html", {"user_submissions": user_submissions})
@login_required
def user_submissions(request):
    submissions = CodeSubmission.objects.filter(user=request.user).select_related('problem').order_by('-created_at')
    return render(request, 'user_submissions.html', {'submissions': submissions})



@login_required
def view_submission(request, submission_id):
    submission = get_object_or_404(CodeSubmission, id=submission_id, user=request.user)
    return render(request, 'view_submission.html', {'submission': submission})

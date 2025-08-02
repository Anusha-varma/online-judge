from django.shortcuts import render, get_object_or_404, redirect
from .models import Problem, Contest, CodeSubmission
from django.db.models import Q
from .forms import CodeSubmissionForm, ProblemForm, ContestForm
import os
import uuid
import subprocess
from pathlib import Path
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import generate_master_code
from dotenv import load_dotenv
from django.utils import timezone
from django.contrib import messages
from django.utils.timezone import localtime

load_dotenv()

def is_admin(user):
    return user.is_superuser or user.is_staff

def problems_list(request):
    query = request.GET.get("q")
    difficulty = request.GET.get("difficulty")
    company = request.GET.get("company")

    user_profile = request.user.profile
    level = user_profile.level
    now = timezone.now()

    problems = Problem.objects.filter(level=level)

    if difficulty:
        problems = problems.filter(difficulty__iexact=difficulty)
    if query:
        problems = problems.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if company:
        problems = problems.filter(company__iexact=company)

    return render(request, 'ProblemsList.html', {
        'problems': problems,
        "user_level": level,
        'selected': difficulty,
        'query': query or '',
        'now': now,
        'is_authenticated': request.user.is_authenticated,
    })

def problem_details(request, id):
    problem = get_object_or_404(Problem, id=id)

    output = None
    expected_output = None
    verdict = None

    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            if request.user.is_authenticated:
                submission.user = request.user
            submission.problem = problem

            output = run_code(
                submission.language,
                code=submission.code,
                input_data=submission.input_data or problem.test_input
            )
            submission.output_data = output
            submission.save()

            master_path = os.path.join(settings.BASE_DIR, "solutions", f"solution_{problem.id}.{submission.language}")
            if os.path.exists(master_path):
                expected_output = run_code(
                    submission.language,
                    filepath=master_path,
                    input_data=submission.input_data or problem.test_input
                )
                if output.strip() == expected_output.strip():
                    verdict = "Accepted ✅"
                else:
                    verdict = "Wrong Answer ❌"

                already_scored = CodeSubmission.objects.filter(
                    user=request.user,
                    problem=problem,
                    score=100
                ).exists()
                submission.score = 100 if verdict == "Accepted ✅" and not already_scored else 0
                submission.save()
    else:
        form = CodeSubmissionForm()

    return render(request, "ProblemDetail.html", {
        "problem": problem,
        "form": form,
        "output": output,
        "expected_output": expected_output,
        "verdict": verdict,
        "show_result": output is not None,
    })



def run_code(language, code=None, input_data="", filepath=None):
    codes_dir = Path("/tmp/codes")
    inputs_dir = Path("/tmp/inputs")
    outputs_dir = Path("/tmp/outputs")

    for directory in [codes_dir, inputs_dir, outputs_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    unique = str(uuid.uuid4())
    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    if filepath is None:
        with open(code_file_path, "w") as f:
            f.write(code)
    else:
        code_file_path = Path(filepath)

    with open(input_file_path, "w") as f:
        f.write(input_data)

    output_file_path.touch()

    try:
        if language in ["cpp", "c"]:
            executable_path = codes_dir / unique
            compiler = "g++" if language == "cpp" else "gcc"
            compile_result = subprocess.run(
                [compiler, str(code_file_path), "-o", str(executable_path)],
                stderr=subprocess.PIPE
            )
            if compile_result.returncode != 0:
                return f"Compilation Error:\n{compile_result.stderr.decode()}"

            with open(input_file_path, "r") as input_file:
                exec_result = subprocess.run(
                    [str(executable_path)],
                    stdin=input_file,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )
                if exec_result.returncode != 0:
                    return f"Runtime Error:\n{exec_result.stderr.decode()}"
                return exec_result.stdout.decode() or "(No Output)"

        elif language == "py":
            with open(input_file_path, "r") as input_file:
                exec_result = subprocess.run(
                    ["python3", str(code_file_path)],
                    stdin=input_file,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5
                )
                if exec_result.returncode != 0:
                    return f"Runtime Error:\n{exec_result.stderr.decode()}"
                return exec_result.stdout.decode() or "(No Output)"

        else:
            return "Unsupported language"

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out"
    except Exception as e:
        return f"Error: {str(e)}"


@login_required
@user_passes_test(is_admin)
def add_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('problems_list')
    else:
        form = ProblemForm()
    return render(request, 'AddProblem.html', {'form': form})

def contests_page(request):
    now = timezone.now()
    upcoming_contests = Contest.objects.filter(start_time__gt=now).order_by('start_time')
    past_contests = Contest.objects.filter(end_time__lt=now).order_by('-end_time')
    return render(request, 'contests_list.html', {
        'upcoming_contests': upcoming_contests,
        'past_contests': past_contests,
    })

def contests_list(request):
    now = timezone.now()
    live_contests = Contest.objects.filter(start_time__lte=now, end_time__gt=now).order_by('start_time')
    upcoming_contests = Contest.objects.filter(start_time__gt=now).order_by('start_time')
    past_contests = Contest.objects.filter(end_time__lte=now).order_by('-end_time')
    return render(request, 'contests_list.html', {
        'upcoming_contests': upcoming_contests,
        'past_contests': past_contests,
        'live_contests': live_contests,
    })

def contest_detail(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)
    now = timezone.now()
    problems = contest.problems.all()
    if contest.start_time > now:
        messages.warning(request, "⏳ This contest hasn’t started yet!")
        return redirect('contests_list')
    return render(request, 'contest_detail.html', {
        'contest': contest,
        'problems': problems,
        'end_time': localtime(contest.end_time).strftime('%Y-%m-%dT%H:%M:%S')
    })

def create_contest(request):
    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contests_list')
    else:
        form = ContestForm()
    return render(request, 'create_contest.html', {'form': form})

def contest_results(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)
    problems = contest.problems.all()
    submissions = CodeSubmission.objects.filter(problem__in=problems).select_related('user', 'problem')

    user_scores = {}
    for submission in submissions:
        user = submission.user
        user_scores[user] = user_scores.get(user, 0) + submission.score

    sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)

    return render(request, 'contest_results.html', {
        'contest': contest,
        'problems': problems,
        'submissions': submissions,
        'leaderboard': sorted_scores,
    })

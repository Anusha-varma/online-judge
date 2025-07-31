from django.db import models
from django.contrib.auth.models import User


class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=[
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard')
    ])
    level = models.CharField(max_length=20, choices=[
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ],default="Beginner")
    sample_input = models.TextField(null=True, blank=True)
    sample_output = models.TextField(null=True, blank=True)
    test_input = models.TextField(null=True, blank=True)
    expected_output = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    contest = models.ForeignKey('Contest', on_delete=models.SET_NULL, null=True, blank=True, related_name="problems_set")



    def __str__(self):
        return self.title

# Create your models here.
class Contest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    problems = models.ManyToManyField('Problem', related_name='contests')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CodeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE,null=True,blank=True)
    code = models.TextField()
    language = models.CharField(max_length=10)
    input_data = models.TextField(null=True,blank=True)
    output_data = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    score=models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.username} - {self.language} - {self.created_at}"

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='testcases')
    input_data = models.TextField()
    expected_output = models.TextField(blank=True, null=True)  # optional if using master solution
    is_sample = models.BooleanField(default=False)  # show on UI or not

    def __str__(self):
        return f"TestCase for {self.problem.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=[
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced")
    ], default="Beginner")

    def __str__(self):
        return f"{self.user.username} - {self.level}"


class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

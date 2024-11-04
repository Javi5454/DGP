from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

# Create your views here.
def index(request):
    return HttpResponse("Hello World. You are at the polls index.")

def questions(request):
    all_questions = Question.objects.all()
    context = {
        "all_questions" : all_questions,
    }
    return render(request, "questions.html", context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import DinnerTask
from .forms import DinnerTaskForm

# Create your views here.

def is_teacher_or_admin(user):
    '''Check if the user is a teacher or admin'''
    try:
        return user.person.role in ['teacher', 'admin']
    except:
        return False
    
@user_passes_test(is_teacher_or_admin)
def create_dinner_task(request):
    if request.method == 'POST':
        form = DinnerTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dinner_task_list')
    else:
        form = DinnerTaskForm()
    return render(request, 'create_dinner_task.html', {'form':form})
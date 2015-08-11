from django.shortcuts import render
from .form import StudentForm
# Create your views here.

def student_create(request):
    if request.method == 'GET':
        form = StudentForm()
        return render(request, 'student/student_create.html', context={'form': form})
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'student/student_create.html', context={'form': form})

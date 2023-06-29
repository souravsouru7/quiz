from django.shortcuts import render, get_object_or_404,redirect
from .models import Quiz, Question, Answer
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import LoginForm, RegistrationForm

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    context = {'quiz': quiz, 'questions': questions}
    return render(request, 'quiz/quiz_detail.html', context)


def submit_answer(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    total_marks = 0

    for question in questions:
        selected_answer_id = request.POST.get(f'answer_{question.id}')
        try:
            selected_answer = question.answer_set.get(id=selected_answer_id)
        except Answer.DoesNotExist:
            return HttpResponse("Invalid answer selected.")
        
        if selected_answer.is_correct:
            total_marks += 1

    context = {'quiz': quiz, 'total_marks': total_marks}
    return render(request, 'quiz/result.html', context)

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

# Other view functions...

def generate_certificate(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # Retrieve user information or any other relevant data for the certificate
    # Customize the certificate template using the retrieved data

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    
    # Generate the PDF
    p = canvas.Canvas(response)
    
    # Customize the certificate design using ReportLab
    p.setFont("Helvetica", 24)
    p.drawString(100, 750, "Certificate of Completion")
    
    p.setFont("Helvetica", 14)
    p.drawString(100, 700, "This is to certify that")
    p.drawString(100, 675, "John Doe")
    p.drawString(100, 650, "has successfully completed the")
    p.drawString(100, 625, f"{quiz.title} Quiz")

    p.showPage()
    p.save()
    return 


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('quiz_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'quiz/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'quiz/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('quiz_list')
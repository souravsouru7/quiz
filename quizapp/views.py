
# quiz/views.py
# quiz/views.py
from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question,Answer

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
        selected_answer = get_object_or_404(Answer, id=selected_answer_id)
        if selected_answer.is_correct:
            total_marks += 1

    context = {'quiz': quiz, 'total_marks': total_marks}
    return render(request, 'quiz/result.html', context)

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

# Other view functions...

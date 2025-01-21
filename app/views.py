from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import Question, Tag
from .utils import paginate_queryset

def index(request):
    questions = Question.objects.new_questions()
    page_number = request.GET.get('page', 1)
    questions_paginated, paginator = paginate_queryset(questions, page_number, 10)

    return render(request, 'index.html', {
        'questions': questions_paginated,
        'paginator': paginator,
    })

# Это из ТЗ 2 вк имитация БД
# QUESTIONS = [
#     {
#         'title': f'title {i}',
#         'id': i,
#         'text': 'This is text for question {i}'
#     } for i in range(1, 30)
# ]


# def index(request):  # принимает на вход запрос от пользователя
#     return render(
#         request, 'index.html',
#         context={'questions': QUESTIONS}
#     )

# Cоздаём словарь, где ключом является строка 'questions', а значением — список вопросов.
# В шаблоне index.html
# Можно получить доступ к этому списку, используя синтаксис шаблонов Django.

# def paginate(request, queryset, per_page=10):
#     paginator = Paginator(queryset, per_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return page_obj

def new_questions(request):
    questions = Question.objects.new_questions()  # Получаем новые вопросы из ModelManager
    page = request.GET.get('page', 1)  # Получаем номер страницы из параметра запроса
    questions_paginated, paginator = paginate_queryset(questions, page, 10)  # Пагинация

    return render(request, 'questions/new_questions.html', {
        'questions': questions_paginated,
        'paginator': paginator,
    })

# def new_questions(request):
#     questions = Question.objects.new_questions()
#     return render(request, 'questions_list.html', {'questions': questions})

def new_questions(request):
    questions = Question.objects.new_questions()
    page_obj = paginate(request, questions)
    return render(request, 'questions_list.html', {'page_obj': page_obj})


def best_questions(request):
    questions = Question.objects.best_questions()
    return render(request, 'questions_list.html', {'questions': questions})

def questions_by_tag(request, tag_name):
    questions = Question.objects.by_tag(tag_name)
    return render(request, 'questions_list.html', {'questions': questions, 'tag': tag_name})

# def hot(request):
#     return render(request, 'hot.html', context={'questions': QUESTIONS})
#
#
# def tag(request, tag):
#     return render(request, 'tag.html', context={'questions': QUESTIONS, 'tag': tag})


def question(request, question_id):
    return render(request, 'question.html', context={'question': question})


def login(request):
    return render(request, 'login.html', context=None)


def signup(request):
    return render(request, 'signup.html', context=None)


def ask(request):
    return render(request, 'ask.html', context=None)
# мб убрать None



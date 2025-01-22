from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .utils import paginate_queryset
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm
from .models import Tag

def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                auth_login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('index')
            else:
                form.add_error(None, "Wrong login or password!")
    else:
        form = LoginForm()

    context = {
        "content_title": "Login",
        "form": form,
        "popular_tags": Tag.objects.get_popular(),  # Предположим, что вы создали метод get_popular() в модели Tag
        # "popular_users": BestMember.objects.all().order_by('-total_score')[:5]  # Пример с популярными пользователями
    }
    return render(request, 'login.html', context)


# def logout(request):
#     next_page = request.META.get('HTTP_REFERER', None)  # Получаем предыдущий URL
#     auth_logout(request)
#
#     if next_page:
#         return redirect(next_page)  # Если была страница, с которой пришел пользователь, возвращаем его на неё
#     return redirect('index')  # Если нет — на главную страницу
#
# def index(request):
#     questions = Question.objects.new_questions()
#     page_number = request.GET.get('page', 1)
#     questions_paginated, paginator = paginate_queryset(questions, page_number, 10)
#
#     return render(request, 'index.html', {
#         'questions': questions_paginated,
#         'paginator': paginator,
#     })

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



from django.shortcuts import render

# Это из ТЗ 2 вк имитация БД
QUESTIONS = [
    {
        'title': f'title {i}',
        'id': i,
        'text': 'This is text for question {i}'
    } for i in range(1, 30)
]


def index(request):  # принимает на вход запрос от пользователя
    return render(
        request, 'index.html',
        context={'questions': QUESTIONS}
    )


# Cоздаём словарь, где ключом является строка 'questions', а значением — список вопросов.
# В шаблоне index.html
# Можно получить доступ к этому списку, используя синтаксис шаблонов Django.

def hot(request):
    return render(request, 'hot.html', context={'questions': QUESTIONS})


def tag(request, tag):
    return render(request, 'tag.html', context={'questions': QUESTIONS, 'tag': tag})


def question(request, question_id):
    return render(request, 'question.html', context={'question': question})


def login(request):
    return render(request, 'login.html', context=None)


def signup(request):
    return render(request, 'signup.html', context=None)


def ask(request):
    return render(request, 'ask.html', context=None)
# мб убрать None

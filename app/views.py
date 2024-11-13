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
# Вы создаете словарь, где ключом является строка 'questions', а значением — список вопросов.
# В шаблоне index.html
# вы можете получить доступ к этому списку, используя синтаксис шаблонов Django.
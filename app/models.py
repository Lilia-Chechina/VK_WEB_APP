from django.db import models

class Profile(models.Model):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.jpg')
    # будет сохраняться в папке avatar

    def __str__(self):
        return self.nickname # может возвращать с f-строкой
    # тут бы по-хорошему нормально всё возвращать


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    # если автор удаляет свой профиль, то вопросы, созданные им, будут оставаться в базе данных,
    # но поле author будет равно NULL
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='questions' # имя обратной связи
        # через questions на объекте Profile можно получить все вопросы, которые были заданы этим пользователем
    )
    # author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions')
    score = models.IntegerField(default=0)  # Счётчик голосов
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')  # если вопрос будет удалён,
    # то связанные с ним ответы будут удалены
    # answers – имя обратной связи, через объект Question можно будет получить все ответы, связанные с этим вопросом
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='answers')  # если удалить профиль,
    # то ответы останутся
    # user = Profile.objects.get(id=1)
    # user_answers = user.answers.all()  # получим все ответы этого пользователя
    text = models.TextField()
    score = models.IntegerField(default=0)  # Счётчик голосов за ответ
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.title}"


class BestMember(models.Model):
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)  # если удалить профиль, то уберём из BestMembers
    total_answers = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)

    def update_score(self):
        # для пересчета рейтинга спустя время
        self.total_answers = self.member.answers.count()
        self.total_score = sum(answer.score for answer in self.member.answers.all())
        self.save()

    def __str__(self):
        return self.member.nickname

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# в PostgreSQL все названия таблиц в строчных буквах в стиле app_profile

# post_save для связи между user и Profile, чтобы при создании Profile создавался и user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.jpg')
    # будет сохраняться в папке avatar

    def __str__(self):
        return self.user.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def best_questions(self):
        return self.order_by('-score')

    def new_questions(self):
        return self.order_by('-created')

    def by_tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-created')

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
    objects = QuestionManager()  # для лучших и новых вопросов

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.id})

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

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes') # все лайки пользователя
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='likes')  # все лайки вопроса
    created = models.DateTimeField(auto_now_add=True)
    value = models.SmallIntegerField(default=0)

    class Meta:  # для добавления ограничений
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_question_like')  #  один и тот же
            # пользователь (user) не может поставить лайк на один и тот же вопрос (question) дважды.
        ]

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)
    value = models.SmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'answer'], name='unique_answer_like')
        ]
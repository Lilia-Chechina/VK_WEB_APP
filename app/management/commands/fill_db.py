from django.core.management.base import BaseCommand, CommandError
from app.models import Profile, Tag, Question, QuestionLike, Answer, AnswerLike, User

from random import randint
from django.contrib.auth.hashers import make_password

USERS = ["Lilia", "Vera", "Nastya", "Max", "Kolyan", "Anton", "Ultius", "Boris", "Cruella"]
TAGS = ["C++", "Django", "Pearl", "Prolog", "Swift", "Rust", "Linux", "ML", "PostgreSQL"]
TITLES = ["MAI", "People", "Love", "Kaif", "Streshka", "Trump", "IlonMask", "VK"]
TEXTS = ["I want sleep", "Help!", "I love C++", "I handed over OOP to C ++", "WOW", "I don't leave the house for weeks and live on deliveries.", "I like LSP",
         "My friends tell me that I'll soon become a vampire because I don't go out enough",
         "Do I wanna know?"]

DEFAULT_PASSWORD = "bebebebe"


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('total', type=int)

    @staticmethod
    def create_profiles(count):
        users = [
            User(
                username=f"{USERS[i % len(USERS)]}{i}",
                password=make_password(DEFAULT_PASSWORD)
            ) for i in range(count)
        ]
        User.objects.bulk_create(users)
        profiles = [Profile(user=users[i]) for i in range(count)]
        Profile.objects.bulk_create(profiles)
        return profiles

    @staticmethod
    def create_tags(count):
        Tag.objects.bulk_create([Tag(name=f"{TAGS[i % len(TAGS)]} {i}") for i in range(count)])

    @staticmethod
    def create_answer_likes(ratio):
        existing_likes = set(
            AnswerLike.objects.values_list('user_id', 'answer_id')
        )
        new_likes = []
        for i in range(100 * ratio):
            user_id = i % ratio + 1
            answer_id = i % (100 * ratio) + 1
            value = 2 * (i % 2) - 1  # +1 или -1
            if (user_id, answer_id) not in existing_likes:
                new_likes.append(AnswerLike(user_id=user_id, answer_id=answer_id, value=value))
                existing_likes.add((user_id, answer_id))  # Обновляем множество
        AnswerLike.objects.bulk_create(new_likes)

    @staticmethod
    def create_question_likes(ratio):
        existing_likes = set(
            QuestionLike.objects.values_list('user_id', 'question_id')
        )
        new_likes = []
        for i in range(10 * ratio):
            user_id = i % ratio + 1
            question_id = i % (10 * ratio) + 1
            value = 2 * (i % 2) - 1  # +1 или -1
            if (user_id, question_id) not in existing_likes:
                new_likes.append(QuestionLike(user_id=user_id, question_id=question_id, value=value))
                existing_likes.add((user_id, question_id))
        QuestionLike.objects.bulk_create(new_likes)

    def handle(self, *args, **options):
        ratio = int(options["total"])
        profiles = self.create_profiles(ratio)

        self.create_tags(ratio)

        range_start = randint(0, ratio // 3)
        offset = 5 if ratio > 5 else ratio
        random_tags = Tag.objects.filter(id__gte=range_start).all()[:offset]

        for j in range(10):
            questions = Question.objects.bulk_create([
                Question(
                    author_id=profiles[(j * i) % ratio].id,
                    title=TITLES[(j * i) % len(TITLES)],
                    text=TEXTS[(j * i) % len(TEXTS)],
                ) for i in range(ratio)
            ])

            through_model_instances = [
                Question.tags.through(question=question, tag=tag)
                for question, tag in zip(questions, random_tags)
            ]

            Question.tags.through.objects.bulk_create(through_model_instances)

        for j in range(100):
            Answer.objects.bulk_create([
                Answer(
                    question_id=((i + 1) * j) % (10 * ratio) + 1,
                    author_id=profiles[(j * i) % ratio].id,
                    text=TEXTS[(j * i) % len(TEXTS)]
                ) for i in range(ratio)
            ])

        self.create_question_likes(ratio)
        self.create_answer_likes(ratio)

        print("OK!")





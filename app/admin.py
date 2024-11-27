from django.contrib import admin
from .models import Profile

admin.site.register(Profile)


# # Класс для настройки отображения модели Profile в админке
# class ProfileAdmin(admin.ModelAdmin):
#     # Определяем поля, которые будут отображаться в списке объектов в админке
#     list_display = (
#     'email', 'nickname', 'password', 'avatar')  # Здесь указаны те поля, которые мы хотим видеть в списке
#
#     # возможность поиска по email и nickname
#     search_fields = ('email', 'nickname')
#
#     # фильтрация по полям (например, фильтрация по avatar)
#     list_filter = ('avatar',)
#
#     # Указываем поля, которые будут редактироваться в форме
#     fields = ('email', 'nickname', 'password', 'avatar')
#
#
# # Регистрируем модель Profile в админке с настройками ProfileAdmin
# admin.site.register(Profile, ProfileAdmin)

from django.contrib import admin

from .models import Answer, Category, Question, Quiz, TakenQuiz, UserAnswer


class AnswerInline(admin.TabularInline):
    model = Answer
    min_num = 2
    extra = 0


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('title', )
    fields = ('title', 'slug', 'description')
    prepopulated_fields = {
        'slug': ('title', )
    }


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_public')
    fields = ('title', 'author', 'slug', 'description', 'category', 'is_public', 'created')
    readonly_fields = ('created', )
    list_editable = ('is_public', )
    prepopulated_fields = {
        'slug': ('title', )
    }


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'quiz')
    fields = ('quiz', 'title', 'image')
    inlines = (AnswerInline, )


admin.site.register(UserAnswer)
admin.site.register(TakenQuiz)

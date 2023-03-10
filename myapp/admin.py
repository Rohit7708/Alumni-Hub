from django.contrib import admin
from .models import *

# Register your models here.

#my admin
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Category)

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display=['question','level']
    
admin.site.register(QuizQuestion,QuizQuestionAdmin)

class UserSubmittedAnswerAdmin(admin.ModelAdmin):
    list_display=['id','question','user','right_answer']

admin.site.register(UserSubmittedAnswer,UserSubmittedAnswerAdmin)

admin.site.register(UserCategoryAttempts)



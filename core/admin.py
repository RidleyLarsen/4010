from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from core.models import Quiz, QuizAnswer, QuizQuestion


class QuizAnswerInline(NestedStackedInline):
    model = QuizAnswer
    fk_name = 'question'
    extra = 1


class QuizQuestionInline(NestedStackedInline):
    model = QuizQuestion
    extra = 1
    fk_name = 'quiz'
    inlines = [QuizAnswerInline]


class QuizAdmin(NestedModelAdmin):
    model = Quiz
    inlines = [QuizQuestionInline]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(QuizAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


# class LevelTwoInline(NestedStackedInline):
#     model = LevelTwo
#     extra = 1
#     fk_name = 'level'
#     inlines = [LevelThreeInline]

# class PassengerInline(admin.StackedInline):
#     model = Passenger
#     fields = (
#         'name',
#         'email',
#         'address_1',
#         'address_2',
#         'city',
#         'state',
#         'zip_code',
#         'phone',
#         'num_passengers',
#         'notes',
#         'email_or_text',
#         'return_ride',
#         'profile',
#         'link',
#         'email_link',
#         'return_ride_link',
#     )
#     readonly_fields = ('link', 'email_link', 'return_ride_link', )
#     extra = 1


# class RideAdmin(admin.ModelAdmin):
#     list_filter = ('date', 'schedule__destination', 'schedule__starting_point')
#     inlines = [PassengerInline]
#     list_display = ('starting_point', 'destination', 'date', 'total_passengers', 'seats_available')



# Register your models here.
admin.site.register(Quiz, QuizAdmin)
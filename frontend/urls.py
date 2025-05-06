from django.urls import path
from .views import home_view,flashcards_view,quizzes_view,study_plan_view

urlpatterns = [
    path('', home_view, name='home'),
    path('flashcards/', flashcards_view, name='flashcards'),
    path('quizzes/', quizzes_view, name='quizzes'),
    path('study-plan/', study_plan_view, name='study_plan'),

]

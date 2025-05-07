from django.urls import path
from .views import home_view,flashcards_view,study_plan_view , translate_pdf_to_flashcard,translate_pdf_to_quiz,translate_pdf_to_studyplan

urlpatterns = [
    path('', home_view, name='home'),
    path('flashcards/', flashcards_view, name='flashcards'),
    # path('quizzes/', quizzes_view, name='quizzes'),
    path('study-plan/', study_plan_view, name='study_plan'),
    path('upload-flashcards/', translate_pdf_to_flashcard, name='upload_flashcards'),
    path('upload-quizzes/', translate_pdf_to_quiz, name='upload_quizzes'),
    path("upload-studyplan/", translate_pdf_to_studyplan, name="upload-studyplan"),
]

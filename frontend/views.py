
# Create your views here.
from django.shortcuts import render
import json
from django.shortcuts import render, get_object_or_404
from .models import Course, StudyWeek, Deliverable, EvaluationItem

from datetime import date

def home_view(request):
    services = [
        {'name': 'PDF Analyzer', 'description': 'Extract key content from PDF files','url':''},
        {'name': 'AI Flashcards', 'description': 'Generate smart flashcards from text','url':'flashcards'},
        {'name': 'Quiz Generator', 'description': 'Create practice quizzes instantly','url':'quizzes'}
    ]

    team = [
        {'name': 'Ajlan', 'linkedin': 'https://linkedin.com/in/ali-mutairi'},
        {'name': 'Hamad', 'linkedin': 'https://linkedin.com/in/sara-qahtani'},
        {'name': 'Faris', 'linkedin': 'https://linkedin.com/in/yousef-fahad'},
        {'name': 'Abdullah', 'linkedin': 'https://linkedin.com/in/yousef-fahad'}
    ]

    return render(request, 'frontend/home.html', {'services': services, 'team': team})


def flashcards_view(request):
    team = [
        {'name': 'Ajlan', 'linkedin': 'https://linkedin.com/in/ali-mutairi'},
        {'name': 'Hamad', 'linkedin': 'https://linkedin.com/in/sara-qahtani'},
        {'name': 'Faris', 'linkedin': 'https://linkedin.com/in/yousef-fahad'},
        {'name': 'Abdullah', 'linkedin': 'https://linkedin.com/in/yousef-fahad'}
    ]

    flashcards = [
        {"title": "HTTP", "definition": "HyperText Transfer Protocol"},
        {"title": "API", "definition": "Application Programming Interface"},
        {"title": "JSON", "definition": "JavaScript Object Notation"},
    ]
    return render(request, 'frontend/flashcards.html', {"flashcards": flashcards, 'team': team})



def quizzes_view(request):
    team = [
        {'name': 'Ajlan', 'linkedin': 'https://linkedin.com/in/ali-mutairi'},
        {'name': 'Hamad', 'linkedin': 'https://linkedin.com/in/sara-qahtani'},
        {'name': 'Faris', 'linkedin': 'https://linkedin.com/in/yousef-fahad'},
        {'name': 'Abdullah', 'linkedin': 'https://linkedin.com/in/yousef-fahad'}
    ]

    questions = [
        {
            'question': 'What is 2+2?',
            'choices': ['3', '4', '5'],
            'correct': '4'
        },
        {
            'question': 'What is 2+2?',
            'choices': ['3', '4', '5'],
            'correct': '4'
        },
        {
            'question': 'What is 2+2?',
            'choices': ['3', '4', '5'],
            'correct': '4'
        },
        {
            'question': 'What is 2+2?',
            'choices': ['3', '4', '5'],
            'correct': '4'
        },
        {
            'question': 'What is 2+2?',
            'choices': ['3', '4', '5'],
            'correct': '4'
        },
        {
            'question': 'What is 2+2?',
            'choices': ['3', '4', '5'],
            'correct': '4'
        },
        {
            'question': 'What is 2+2?',
            'choices': ['3', '4', '5'],
            'correct': '4'
        },
        # Add more questions...
    ]
    correct_answers = [q['correct'] for q in questions]
    return render(request, 'frontend/quizzes.html', {
        'questions': questions,
        'correct_answers': json.dumps(correct_answers),  # Convert to JSON
        'team': team
    })




from django.shortcuts import render

def study_plan_view(request):
    # Hardcoded course data
    course = {
        'name': 'Advanced Mathematics',
        'recommended_study_time': '6-8 hours outside class'
    }

    # Hardcoded study plan data
    study_plan = {
        'weeks': [
            {
                'number': 1,
                'topics': 'Linear Algebra basics, Matrix operations',
                'tasks': 'Read chapter 1, Complete problem set 1',
                'resources': 'Textbook chapters 1-2, Lecture slides week 1',
                'tips': 'Focus on understanding matrix multiplication fundamentals'
            },
            {
                'number': 2,
                'topics': 'Vector spaces, Linear transformations',
                'tasks': 'Read chapter 2, Complete problem set 2',
                'resources': 'Textbook chapter 3, Supplementary videos',
                'tips': 'Draw diagrams to visualize vector spaces'
            },
            # Add more weeks as needed...
        ],
        'deliverables': [
            {'name': 'Problem Set 1', 'week': 1},
            {'name': 'Matrix Project', 'week': 3},
            # Add more deliverables...
        ],
        'evaluation': [
            {'name': 'Midterm Exam', 'percentage': 30},
            {'name': 'Assignments', 'percentage': 20},
            {'name': 'Group Project', 'percentage': 20},
            {'name': 'Final Exam', 'percentage': 30},
        ]
    }

    semester_start = date(2023, 9, 1)  # Adjust to your semester start
    today = date.today()
    current_week = min(((today - semester_start).days // 7) + 1, 12)

    return render(request, 'frontend/study-plan.html', {
        'course': course,
        'study_plan': study_plan,
        'current_week': 1 # You can calculate this dynamically
    })


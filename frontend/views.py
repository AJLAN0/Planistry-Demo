
# Create your views here.
from django.shortcuts import render
import json
from django.shortcuts import render, get_object_or_404
from .models import Course, StudyWeek, Deliverable, EvaluationItem
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
import os
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import re


from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def home_view(request):
    services = [
    {
        'name': 'Study Plan Generator',
        'description': 'Automatically create weekly study plans from your syllabus with tasks, topics, and resources.',
        'url': 'study-plan'
    },
    {
        'name': 'Flashcards Generator',
        'description': 'Turn your lecture notes or PDFs into interactive flashcards to boost memory retention.',
        'url': 'flashcards'
    },
    {
        'name': 'Quiz Generator',
        'description': 'Instantly generate multiple-choice quizzes from study material to test your understanding.',
        'url': 'quizzes'
    }
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


def split_text(text, max_length=5000):
    """Splits text into smaller chunks within the character limit."""
    chunks = []
    while len(text) > max_length:
        split_index = text.rfind(" ", 0, max_length)  # Split at the last space before the limit
        if split_index == -1:
            split_index = max_length  # Force split if no space found
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)  # Append the remaining part
    return chunks



def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

def safe_extract_flashcards(raw):
    try:
        # Try full JSON parse
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: try to extract array content using regex
        match = re.search(r"\[\s*{.*?}\s*\]", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return []
        return []


def generate_flashcard_from_text(text):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-zero:free",
            messages=[
                {"role": "system", "content": "You are a JSON API. Return only valid JSON. No explanations, no markdown."},
{"role": "user", "content": (
    "Return exactly 10 flashcards as a JSON array like:\n"
    "[{\"term\": \"\", \"definition\": \"\"}, ...]\n\n"
    f"Text:\n{text}"
)}
            ],
            max_tokens=1500
        )

        print("📦 Full API Response:", response)

        choices = getattr(response, "choices", [])
        if not choices:
            raise ValueError("LLM returned empty choices list.")

        message = choices[0].message
        if not message or not hasattr(message, "content"):
            raise ValueError("LLM response has no content.")

        content = message.content.strip()
        print("💬 Raw content:\n", content)

        # ✂ Remove any leading non-JSON (markdown, \boxed{}, etc.)
        if content.startswith("\\boxed{"):
            content = content[len("\\boxed{"):]

# Remove markdown code block formatting
        content = content.replace("```json", "").replace("```", "").strip()

        # 🔎 Extract only the JSON array part
        matches = re.findall(r"\[\s*{[\s\S]*?}\s*]", content)
        if not matches:
            raise ValueError("No valid JSON array found in response.")

        parsed = json.loads(matches[0])

        flashcards = [
            {"title": fc.get("term", "").strip(), "definition": fc.get("definition", "").strip()}
            for fc in parsed if isinstance(fc, dict) and fc.get("term") and fc.get("definition")
        ]

        return flashcards

    except Exception as e:
        print("❌ Flashcard generation error:", e)
        return {"error": f"Failed to generate flashcards: {str(e)}"}




def translate_pdf_to_flashcard(request):
    """Django function that extracts text from a PDF, translates it in chunks, and generates flashcards."""
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']

        # Save the uploaded file temporarily
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(filename)

        try:
            # Step 1: Extract text from the PDF
            extracted_text = extract_text_from_pdf(file_path)

            if not extracted_text.strip():
                return render(request, 'frontend/flashcards.html', {'status': 'error', 'message': 'No extractable text found in the PDF'})

            # Step 2: Split text into chunks of max 5000 characters
            text_chunks = split_text(extracted_text, max_length=5000)

            # Step 3: Translate each chunk separately
            translator = GoogleTranslator(source='auto', target='en')
            translated_chunks = [translator.translate(chunk) for chunk in text_chunks]

            # Step 4: Merge the translated chunks
            translated_text = " ".join(translated_chunks)

            # Step 5: Generate flashcard from the translated text
            flashcards = generate_flashcard_from_text(translated_text)

            # Log for debugging
            print("Generated flashcards:", flashcards)  # Log the flashcards to check their structure

        except Exception as e:
            return render(request, 'frontend/flashcards.html', {'status': 'error', 'message': str(e)})

        finally:
            # Delete the uploaded file after processing
            if os.path.exists(file_path):
                os.remove(file_path)

        # Check if the flashcards are correctly generated
        # After generating flashcards
        if isinstance(flashcards, dict) and "error" in flashcards:
            return render(request, 'frontend/flashcards.html', {
                'status': 'error',
                'message': flashcards['error']
            })

        # If flashcards is a valid list
        if isinstance(flashcards, list):
            return render(request, 'frontend/flashcards.html', {
                "flashcards": flashcards,
            })

        # Fallback error
        return render(request, 'frontend/flashcards.html', {
            'status': 'error',
            'message': 'Unknown error while generating flashcards.'
        })




def generate_quiz_from_text(text):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-zero:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON API. Return only valid JSON. No explanations, no markdown."
                },
                {
                    "role": "user",
                    "content": (
                        "Return exactly 5 multiple-choice questions as JSON array like:\n"
                        "[{\"question\": \"...\", \"choices\": [\"...\"], \"answer\": \"...\"}]\n\n"
                        f"Text:\n{text}"
                    )
                }
            ],
            max_tokens=1500
        )

        content = getattr(response.choices[0].message, "content", "").strip()
        print("💬 Raw content:\n", content)

        # Step 1: Clean known wrappers
        content = content.replace("\\boxed{", "").replace("```json", "").replace("```", "").strip("} \n")

        # Step 2: Find the longest valid JSON list
        match = re.search(r"\[\s*{[\s\S]+?}\s*\]", content)
        if not match:
            raise ValueError("No valid JSON array found")

        # Step 3: Attempt to parse the JSON array
        raw_array = match.group(0)
        try:
            parsed = json.loads(raw_array)
        except json.JSONDecodeError:
            # Try partial recovery: cut before last invalid JSON comma or object
            trimmed = raw_array.rsplit("},", 1)[0] + "}]"
            parsed = json.loads(trimmed)

        # Step 4: Normalize the result
        questions = [
            {
                "question": q.get("question", "").strip(),
                "choices": q.get("choices", []),
                "correct": q.get("answer", "").strip()
            }
            for q in parsed if isinstance(q, dict) and q.get("question") and q.get("choices") and q.get("answer")
        ]

        return questions

    except Exception as e:
        print("❌ Quiz generation error:", e)
        return {"error": f"Failed to generate quiz: {str(e)}"}










def translate_pdf_to_quiz(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(filename)

        try:
            extracted_text = extract_text_from_pdf(file_path)

            if not extracted_text.strip():
                return render(request, 'frontend/quizzes.html', {
                    'status': 'error', 'message': 'No extractable text found.'
                })

            text_chunks = split_text(extracted_text, max_length=5000)
            translator = GoogleTranslator(source='auto', target='en')
            translated_chunks = [translator.translate(chunk) for chunk in text_chunks]
            translated_text = " ".join(translated_chunks)

            questions = generate_quiz_from_text(translated_text)
            print("Generated quiz:", questions)

        except Exception as e:
            return render(request, 'frontend/quizzes.html', {
                'status': 'error', 'message': str(e)
            })

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

        if isinstance(questions, list):
            correct_answers = [q['correct'] for q in questions]
            return render(request, 'frontend/quizzes.html', {
                "questions": questions,
                "correct_answers": json.dumps(correct_answers)
            })
        else:
            return render(request, 'frontend/quizzes.html', {
                'status': 'error',
                'message': 'Failed to generate valid questions.'
            })

    return render(request, 'frontend/quizzes.html')


def generate_studyplan_from_text(text):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-zero:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON API. Return only valid JSON. No explanations or markdown."
                },
                {
                    "role": "user",
                    "content": (
                        "Extract a clean study plan from the following syllabus text.\n"
                        "Return only a valid JSON object with 3 keys: 'weeks', 'deliverables', and 'evaluation'.\n"
                        "Example:\n"
                        "{\n"
                        "  \"weeks\": [{\"number\": 1, \"topics\": \"...\", \"tasks\": \"...\", \"resources\": \"...\", \"tips\": \"...\"}],\n"
                        "  \"deliverables\": [{\"name\": \"Assignment 1\", \"week\": 2}],\n"
                        "  \"evaluation\": [{\"name\": \"Final Exam\", \"percentage\": 40}]\n"
                        "}\n\n"
                        f"Text:\n{text}"
                    )
                }
            ],
            max_tokens=2000
        )

        print("📦 Full Study Plan API Response:", response)

        choices = getattr(response, "choices", [])
        if not choices:
            raise ValueError("LLM returned empty choices list.")

        message = choices[0].message
        if not message or not hasattr(message, "content"):
            raise ValueError("LLM response has no content.")

        content = message.content.strip()
        print("💬 Raw content:\n", content)

        # ✂ Clean known wrappers and markdown
        if content.startswith("\\boxed{"):
            content = content[len("\\boxed{"):].strip("} \n")
        content = content.replace("```json", "").replace("```", "").strip()

        # 🔍 Extract a full JSON object
        match = re.search(r"\{\s*\"weeks\".*?\"evaluation\"\s*:\s*\[.*?\]\s*\}", content, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON object found in response.")

        parsed = json.loads(match.group(0))
        return parsed

    except Exception as e:
        print("❌ Study Plan generation error:", e)
        return {"error": f"Failed to generate study plan: {str(e)}"}




def translate_pdf_to_studyplan(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']

        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(filename)

        try:
            extracted_text = extract_text_from_pdf(file_path)

            if not extracted_text.strip():
                return render(request, 'frontend/study-plan.html', {
                    'status': 'error', 'message': 'No extractable text found in the PDF'
                })

            text_chunks = split_text(extracted_text, max_length=5000)

            translator = GoogleTranslator(source='auto', target='en')
            translated_chunks = [translator.translate(chunk) for chunk in text_chunks]
            translated_text = " ".join(translated_chunks)

            study_plan_data = generate_studyplan_from_text(translated_text)
            print("Generated Study Plan:", study_plan_data)

        except Exception as e:
            return render(request, 'frontend/study-plan.html', {
                'status': 'error', 'message': str(e)
            })

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

        if isinstance(study_plan_data, dict) and "error" in study_plan_data:
            return render(request, 'frontend/study-plan.html', {
                'status': 'error',
                'message': study_plan_data['error']
            })

        return render(request, 'frontend/study-plan.html', {
            'course': {"name": "Auto-generated", "recommended_study_time": "See syllabus"},
            'study_plan': study_plan_data,
            'current_week': 1
        })

    return render(request, 'frontend/study-plan.html', {
        'status': 'error',
        'message': 'Invalid request method or no file uploaded.'
    })

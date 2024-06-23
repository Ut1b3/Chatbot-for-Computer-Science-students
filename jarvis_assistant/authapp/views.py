from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import CustomUser, Reminder, SavedReminder
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ReminderForm
from openai import OpenAI
from django.utils import timezone
from datetime import timedelta
from .models import ChatHistory, Feedback
import json
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from .forms import FeedbackForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the username is a matriculation number or registration number
        try:
            user = CustomUser.objects.get(matric_number__iexact=username)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(reg_number__iexact=username)
            except CustomUser.DoesNotExist:
                user = None

        if user:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Incorrect password.')
        else:
            messages.error(request, 'Invalid matriculation or registration number.')

    return render(request, 'authapp/login.html')

@login_required
def home(request):
    return render(request, 'authapp/home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authapp/register.html', {'form': form})

@login_required
def chatbot(request):
    if request.method == 'GET':
        return render(request, 'authapp/chatbot.html')
    elif request.method == 'POST':
        return HttpResponse(status=200)

@csrf_exempt
@login_required
def chat_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        feedbacks = Feedback.objects.all()
        feedback_messages = [{"role": "user", "content": feedback.feedback_text} for feedback in feedbacks]
        client = OpenAI(api_key="sk-proj-CWA66fwAqeIQVW7dOjvNT3BlbkFJ0xzpyNOsuC4I4gbtpD7D")
        response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    
{"role":"system","content":"You are a helpful assistant kthat provides assistance for Computer Science students at Covenant University."},
*feedback_messages,

    {"role": "system", "content": "You are a helpful assistant that provides assistance for Computer Science students at Covenant University."},

    {"role": "user", "content": "Who is the lecturer for CSC122?"},
    {"role": "assistant", "content": "The lecturer for CSC122: Computer Application Packages II is MISS TUNDE-ADELEKE TI-JESU REJOICE, MR ODUSOTE BABAFEMI OLUBUNMI, MR OKUOYO OTAVIE LOVEDAY, and MRS ABIODUN THERESA NKECHI."},

    {"role": "user", "content": "What is the course code for Introduction to Computational Biology?"},
    {"role": "assistant", "content": "The course code for Introduction to Computational Biology is CSC124."},

    {"role": "user", "content": "List the lecturers for CSC124."},
    {"role": "assistant", "content": "The lecturers for CSC124: Introduction to Computational Biology are DR ISEWON ITUNUOLUWA MARIAN and MISS TUNDE-ADELEKE TI-JESU REJOICE."},

    {"role": "user", "content": "What is the course outline for CSC125?"},
    {"role": "assistant", "content": "The course outline for CSC125: Operating System I includes lectures by MISS NATHANIEL JEMIMAH, MR OGBU HENRY NWAGU, MR OKUOYO OTAVIE LOVEDAY, and PROF OYELADE JELILI OLANREWAJU."},

    {"role": "user", "content": "Who are the lecturers for CSC221?"},
    {"role": "assistant", "content": "The lecturers for CSC221: Computer Programming II are MISS TUNDE-ADELEKE TI-JESU REJOICE, MR ADUBI STEPHEN AYODEJI, MR DADA IBIDAPO DARE, MR EJIOBIH CHUKWUEBUKA JOSHUA, MR JEGEDE TOPE JOHN, and MR OGBU HENRY NWAGU."},

    {"role": "user", "content": "Which lecturers are assigned to CSC223?"},
    {"role": "assistant", "content": "The lecturers for CSC223: Computer Hardware are MR ODUSOTE and MS NATHANIEL."},

    {"role": "user", "content": "Provide the course outline for CSC224."},
    {"role": "assistant", "content": "The course outline for CSC224: Introduction to Computational Biology includes lectures by DR ISEWON ITUNUOLUWA MARIAN and MR OSOFUYE ODUNAYO."},

    {"role": "user", "content": "Who teaches CSC225?"},
    {"role": "assistant", "content": "CSC225: Operating System II is taught by DR JONATHAN OLURANTI, MISS TUNDE-ADELEKE TI-JESU REJOICE, and MR OSOFUYE ODUNAYO."},

    {"role": "user", "content": "Who are the lecturers for CSC227?"},
    {"role": "assistant", "content": "The lecturers for CSC227: Computer Architecture and Organization I are DR JONATHAN OLURANTI and MRS ABIODUN THERESA NKECHI."},

    {"role": "user", "content": "List the lecturers for CSC246."},
    {"role": "assistant", "content": "The lecturers for CSC246: Computer Programming IIA are MISS TUNDE-ADELEKE TI-JESU REJOICE, MR ADUBI STEPHEN AYODEJI, MR DADA IBIDAPO DARE, MR EJIOBIH CHUKWUEBUKA JOSHUA, MR JEGEDE TOPE JOHN, and MR OGBU HENRY NWAGU."},

    {"role": "user", "content": "Who are the lecturers for CSC415?"},
    {"role": "assistant", "content": "The lecturers for CSC415: Artificial Intelligence are DR EZENWOKE AZUBUIKE ANSALEM, MR ADUBI STEPHEN AYODEJI, and MR FRANKLYN EMMANUEL OWAJIYA."},

    {"role": "user", "content": "What is the course code for Concept of Programming Languages?"},
    {"role": "assistant", "content": "The course code for Concept of Programming Languages is CSC423."},

    {"role": "user", "content": "Who teaches CSC424?"},
    {"role": "assistant", "content": "CSC424: Computer Networks/Communication is taught by DR IHEANETU OLAMMA UGOCHI and MR JEGEDE TOPE JOHN."},

    {"role": "user", "content": "What is the course outline for CSC425?"},
    {"role": "assistant", "content": "The course outline for CSC425: Computer Architecture and Organization II includes lectures by DR JONATHAN OLURANTI and MRS ABIODUN THERESA NKECHI."},

    {"role": "user", "content": "Who is responsible for CSC429?"},
    {"role": "assistant", "content": "CSC429: Project is managed by MR EJIOBIH CHUKWUEBUKA JOSHUA."},

    {"role": "user", "content": "Who are the lecturers for CSC441?"},
    {"role": "assistant", "content": "The lecturers for CSC441: Human Computer Interface are DR IHEANETU OLAMMA UGOCHI and MR JEGEDE TOPE JOHN."},

    {"role": "user", "content": "Provide the lecturers for CSC442."},
    {"role": "assistant", "content": "The lecturers for CSC442: Computational Biology and Interdisciplinary Topics are DR ISEWON ITUNUOLUWA MARIAN and MR OSOFUYE ODUNAYO."},

    {"role": "user", "content": "Who teaches CSC121?"},
    {"role": "assistant", "content": "CSC121: Introduction to Problem Solving is taught by DR EZENWOKE AZUBUIKE ANSALEM, MR ADUBI STEPHEN AYODEJI, MR DADA IBIDAPO DARE, MR FRANKLYN EMMANUEL OWAJIYA, MR ODUSOTE BABAFEMI OLUBUNMI, MR OKUOYO OTAVIE LOVEDAY, and PROF OLADIPUPO OLUFUNKE OYEJOKE."},

    {"role": "user", "content": "What are the methods of lecture delivery for CSC 444?"},
    {"role": "assistant", "content": "The methods of lecture delivery for CSC 444 include interactive classroom sessions, group assignments, lecture notes, and the use of charts and diagrams."},

    {"role": "user", "content": "What are the teaching aids used in CSC 444?"},
    {"role": "assistant", "content": "The teaching aids used in CSC 444 include Microsoft PowerPoint slides and the use of a smart board."},

    {"role": "user", "content": "How is a general Computer Science course graded?"},
    {"role": "assistant", "content": f"A Computer Science course is graded with continuous assessment (30 marks), which includes assignments and tests (15%) and a mid-semester exam (15%). The final examination accounts for 70% of the total grade."},

    {"role": "user", "content": "What is the total percentage of the final examination in a Computer Science Program?"},
    {"role": "assistant", "content": f"The final examination accounts for 70% of the total grade."},

    {"role": "user", "content": "What are the ground rules regarding attendance?"},
    {"role": "assistant", "content": f"The ground rules require students to have over 90% average class attendance, with a minimum of 75% attendance to be eligible for exams, and 50% if you are a carry-over student."},

    {"role": "user", "content": "What happens if a student is late for the a lecture?"},
    {"role": "assistant", "content": "Students who are late will not be allowed to enter the class after the lecture has commenced to avoid distractions."},

    {"role": "user", "content": "What is the structure of a Computer Science programme?"},
    {"role": "assistant", "content": "The structure of any programme includes continuous assessment (30 marks) and a final examination (70 marks), totaling 100 marks."},

    {"role": "user", "content": "What are the grades for a CSC course?"},
    {"role": "assistant", "content": "The grades are: \n1. 70-100: A\n2. 60-69: B\n3. 50-59: C\n4. 45-49: D\n Anything below 45: F."},

    {"role": "user", "content": "Who teaches CSC 415 Artificial Intelligence?"},
    {"role": "assistant", "content": "The lecturers for CSC 415: Artificial Intelligence are DR EZENWOKE AZUBUIKE ANSALEM, MR ADUBI STEPHEN AYODEJI, and MR FRANKLYN EMMANUEL OWAJIYA."},

    {"role": "user", "content": "Who is the course coordinator for CSC223?"},
    {"role": "assistant", "content": "The course coordinator for CSC223: Computer Hardware is MR ODUSOTE."},

    {"role": "user", "content": "What topics are covered in CSC121?"},
    {"role": "assistant", "content": "CSC121: Introduction to Problem Solving covers topics such as algorithms, flowcharts, and basic programming concepts."},

    {"role": "user", "content": "What software tools are used in CSC122?"},
    {"role": "assistant", "content": "CSC122: Computer Application Packages II uses software tools like Microsoft Office, Excel, and Access."},

    {"role": "user", "content": "Who is the head of the Computer Science department?"},
    {"role": "assistant", "content": "The head of the Computer Science department is PROF OLADIPUPO OLUFUNKE OYEJOKE."},

    {"role": "user", "content": "What is the duration of the CSC125 lectures?"},
    {"role": "assistant", "content": "The duration of the CSC125: Operating System I lectures is 2 hours per session."},

    {"role": "user", "content": "Which lecturers are assigned to CSC227?"},
    {"role": "assistant", "content": "The lecturers for CSC227: Computer Architecture and Organization I are DR JONATHAN OLURANTI and MRS ABIODUN THERESA NKECHI."},

    {"role": "user", "content": "What are the prerequisites for CSC221?"},
    {"role": "assistant", "content": "The prerequisites for CSC221: Computer Programming II include CSC121 and CSC122."},

    {"role": "user", "content": "What are the assessment methods for CSC225?"},
    {"role": "assistant", "content": "The assessment methods for CSC225: Operating System II include assignments, quizzes, a mid-semester exam, and a final exam."},

    {"role": "user", "content": "What is the grading policy for CSC124?"},
    {"role": "assistant", "content": "The grading policy for CSC124: Introduction to Computational Biology includes continuous assessment (30%) and a final exam (70%)."},

    {"role": "user", "content": "What are the main topics covered in CSC221?"},
    {"role": "assistant", "content": "CSC221: Computer Programming II covers topics such as data structures, algorithms, and object-oriented programming."},
    
    {"role": "user", "content": "Question concerning current course"},
    {"role": "assistant", "content": "Answer concerning current course"},

{"role":"user","content":user_input},

  ],
  temperature=0.3,
    max_tokens=150,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
)
    bot_response = response.choices[0].message.content.strip()
    return JsonResponse({'bot_response': bot_response})
    
@login_required    
def chat_history(request):
    chats = ChatHistory.objects.filter(user=request.user)
    return render(request, 'authapp/chat_history.html', {'chat_history': chats})

@csrf_exempt
@login_required
def save_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        chat_name = data.get('chat_name')
        chat_length = data.get('chat_length')
        chat_history = data.get('chat_history')
        if not chat_name or not chat_history:
            return JsonResponse({'error': 'Invalid data'}, status=400)
        
        chat, created = ChatHistory.objects.get_or_create(
            user=request.user,
            name=chat_name,
            defaults={'length': chat_length, 'history': chat_history}
        )
        if not created:
            chat.length = chat_length
            chat.history = chat_history
            chat.save()
        return JsonResponse({'message': 'Chat saved successfully'})

def view_chat(request, chat_id):
    chat = get_object_or_404(ChatHistory, id=chat_id, user=request.user)
    return render(request, 'authapp/view_chat.html', {'chat': chat})

@csrf_exempt
def delete_chat(request, chat_id):
    if request.method == 'DELETE':
        chat = get_object_or_404(ChatHistory, id=chat_id, user=request.user)
        chat.delete()
        return HttpResponse(status=204)

def about(request):
    return render(request, 'authapp/about.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_reminder(request):
    if request.method == 'POST':
        print(request.POST)  # Debugging: print POST data
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            reminders = Reminder.objects.filter(user=request.user)
            reminder_list = render_to_string('authapp/reminder_list.html', {'reminders': reminders})
            return JsonResponse({'message': 'Reminder saved successfully', 'reminder_list': reminder_list}, status=200)
        else:
            print(form.errors)  # Debugging: print form errors
            return JsonResponse({'message': 'Failed to save reminder', 'errors': form.errors}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=400)


@login_required
def reminders(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reminders')
    else:
        form = ReminderForm()

    reminders = Reminder.objects.filter(user=request.user)
    return render(request, 'authapp/reminders.html', {'form': form, 'reminders': reminders})


def delete_reminder(request, reminder_id):  # Use 'reminder_id' to match the URL pattern
    reminder = Reminder.objects.get(id=reminder_id)
    if reminder.user == request.user:
        reminder.delete()
    return redirect('reminders')

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'feedback.html', {'form': FeedbackForm(), 'message': 'Thank you for your feedback!'})
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

def train_from_feedback():
    feedbacks = Feedback.objects.all()
    feedback_texts = [feedback.feedback_text for feedback in feedbacks]

    # Prepare training data
    training_data = []
    for feedback in feedback_texts:
        training_data.append({"prompt": "User: " + feedback, "completion": "Assistant: "})
    
    # Use OpenAI's API to fine-tune the model (pseudocode)
    client = OpenAI(api_key="sk-proj-CWA66fwAqeIQVW7dOjvNT3BlbkFJ0xzpyNOsuC4I4gbtpD7D")
    response = client.fine_tuning.jobs.create(
    client.client.files.create(
        file=open('training_data.jsonl'),
        model="gpt-3.5-turbo",
        n_epochs=4
    ),
    training_file="file-abc123", 
    model="gpt-3.5-turbo"
    )
    return response
from django.shortcuts import render
from django.http import JsonResponse

from .models import PersonalInfo, HobbyPost
from .forms import ChatForm
from .chatbot import PersonalFactsChatbot

chatbot = PersonalFactsChatbot()


def home(request):
    person = PersonalInfo.objects.first()
    return render(request, 'profileapp/home.html', {'person': person})


def chatbot_view(request):
    form = ChatForm()
    return render(request, 'profileapp/chatbot.html', {'form': form})


def chat_api(request):
    if request.method == 'POST':
        msg = request.POST.get('message', '').strip()
        if not msg:
            return JsonResponse({'reply': "Please type a question about me."})
        answer = chatbot.respond(msg)
        return JsonResponse({'reply': answer})
    return JsonResponse({'error': 'POST only'}, status=405)


def hobbies_view(request):
    person = PersonalInfo.objects.first()
    posts = HobbyPost.objects.filter(person=person, is_published=True)
    return render(
        request,
        'profileapp/hobbies.html',
        {'person': person, 'posts': posts}
    )

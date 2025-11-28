from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import requests

from .models import PersonalInfo, HobbyPost
from .forms import ChatForm


# Simple registry of chatbots for the UI
CHATBOTS = [
    {
        "key": "personal_facts",
        "name": "Level 1 – Personal Facts Bot",
        "tagline": "SentenceTransformer + YAML facts (currently implemented)",
        "description": (
            "This bot answers questions about me by encoding both your question and my "
            "personal facts (from personal_facts.yaml) with SentenceTransformer, then "
            "finding the most similar fact via cosine similarity."
        ),
        "details": (
            "- Model: all-MiniLM-L6-v2 on CPU only\n"
            "- Data source: profileapp/data/personal_facts.yaml (qa + facts)\n"
            "- Pipeline: encode facts → store embeddings → for each question, encode and "
            "compare via cosine similarity → return the closest answer or suggest topics."
        ),
    },
    {
        "key": "gpt2_rag",
        "name": "Level 2 – GPT-2 RAG (Coming soon)",
        "tagline": "Planned: GPT-2-like model + vector DB over personal notes.",
        "description": (
            "Planned upgrade where a small GPT-2-style model will generate answers while "
            "retrieving the most relevant personal notes from a vector database."
        ),
        "details": (
            "- Will use a vector DB (e.g., FAISS/Chroma) for retrieval\n"
            "- Retrieved chunks will be fed into a fine-tuned GPT-2-like model\n"
            "- Good to showcase a lightweight RAG pipeline for personal assistants."
        ),
    },
    {
        "key": "sentencetransformer_qa",
        "name": "Level 3 – Pure Embedding QA (Coming soon)",
        "tagline": "Planned: non-generative QA using SentenceTransformer only.",
        "description": (
            "This planned bot will act as a pure semantic search assistant: it finds the "
            "best matching fact and returns it directly in a curated template, without "
            "any generative model."
        ),
        "details": (
            "- Uses SentenceTransformer only\n"
            "- Fully deterministic, no hallucination, very cheap\n"
            "- Great to demonstrate semantic search without an LLM."
        ),
    },
]

DEFAULT_BOT_KEY = "personal_facts"



def home(request):
    person = PersonalInfo.objects.first()
    return render(request, 'profileapp/home.html', {'person': person})

def _get_active_bot(bot_key: str):
    for b in CHATBOTS:
        if b["key"] == bot_key:
            return b
    return CHATBOTS[0]

def chatbot_view(request):
    form = ChatForm()
    selected_key = request.GET.get('bot', DEFAULT_BOT_KEY)
    active_bot = _get_active_bot(selected_key)

    context = {
        'form': form,
        'chatbots': CHATBOTS,
        'active_bot': active_bot,
    }
    return render(request, 'profileapp/chatbot.html', context)

def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    msg = request.POST.get('message', '').strip()
    bot_key = request.POST.get('bot', '')  # optional, for future multi-bots

    if not msg:
        return JsonResponse({'reply': "Please type a question about me."})

    api_url = getattr(settings, "CHATBOT_API_URL", "http://localhost:8001/api/chat")

    try:
        resp = requests.post(
            api_url,
            json={"message": msg, "bot": bot_key},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        reply = data.get('reply') or "Chatbot service returned no reply."
    except Exception as e:
        # You can log e here if you want
        reply = "Sorry, I couldn't reach the chatbot service right now."

    return JsonResponse({'reply': reply})



def hobbies_view(request):
    person = PersonalInfo.objects.first()
    posts = HobbyPost.objects.filter(person=person, is_published=True)
    return render(
        request,
        'profileapp/hobbies.html',
        {'person': person, 'posts': posts}
    )

def contact_linkedin(request):
    return redirect("https://www.linkedin.com/in/theshankarpoudel/")

def contact_github(request):
    return redirect("https://github.com/ShankarPoudel441")

def resume_view(request):
    return render(request, "profileapp/resume.html")

# Personal Info Django Site + Torch Chatbot

Personal Knowledge Portal + Torch-Powered Retrieval Bot

A compact demonstration of applied AI engineering, full-stack design, and questionable amounts of curiosity.
This project is a lightweight Django web application that serves as a personal information portal while integrating a PyTorch-based semantic retrieval chatbot. The system ingests a structured knowledge file (personal_facts.yaml) and performs sentence-level embedding, vector similarity search, and low-latency response generation using SentenceTransformers.

In simpler terms:
A website where I introduce myself, and a small LLM-adjacent agent trained on my background politely answers questions about me—no cloud APIs harmed in the process.
## Quickstart

```bash
## 🛠️Creating run environment
conda create -n personalai python=3.10
conda activate personalai
pip install -r requirements.txt
## 🚀Launching the Application
cd mysite
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000 to view the site.

The chatbot loads knowledge from: profile_app/data/personal_facts.yml

## 🎯 Purpose of the Project

This system was built primarily to demonstrate:
- AI engineering ability (embedding models, similarity search, inference pipelines).
- Full-stack development (Django, templates, REST endpoints).
- Software craftsmanship (clean architecture, modular components).
- Research alignment with topics such as RAG, efficient model deployment, and agent-centric design.

And also to confirm that even a small personal assistant can exhibit slightly better memory than the average graduate student.😉

## How the Chatbot Works
### Sentence Transformer Chatbot:
- Uses `sentence-transformers` (PyTorch backend) to embed your questions and the bot's knowledge.
- Performs cosine similarity to pick the closest answer.
- No remote calls; everything runs locally.
- Edit `profileapp/data/personal_facts.yaml`; restart the server to reload.

### LLM based:  (Ongoing..) [Deploy on Nov 25, 2025]
- Uses a transferred knowledge from pretrained GPT2, then finetuned for personal dat
- Generate the vector db of `profileapp/data/personal_facts.yaml` and use it for AUG implementation
- Used pretrained model 
## Project Structure

```
mysite/
  manage.py
  mysite/
    settings.py / urls.py / wsgi.py
  profileapp/
    models.py / views.py / urls.py / admin.py / forms.py / chatbot.py
    templates/profileapp/
      base.html / home.html / chatbot.html
    static/profileapp/
    data/personal_facts.yaml
requirements.txt
```

## 📚 Academic Angle

The project represents a micro-scale implementation of retrieval-augmented semantic reasoning, suitable for showcasing competence in:

- Representation learning
- Knowledge encoding
- Python systems design
- Web-AI integration
- Practical ML tooling & reproducible pipelines

It also serves as evidence that I can build functioning systems without resorting to “just run it on Colab and pray.”
 
## 🧩 Future Extensions

- Knowledge-graph integration
- Fine-tuned encoder models
- Agentic workflow orchestration
- Vision-language expansion (inevitable)


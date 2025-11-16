# Personal Info Django Site + Torch Chatbot

A minimal Django project for your personal profile plus a Torch-backed retrieval chatbot trained on your own facts.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd mysite
python manage.py migrate
python manage.py createsuperuser  # optional, for admin
python manage.py runserver
```

Open http://127.0.0.1:8000 to view the site.

## Populate Your Profile

1. Visit `/admin/` and create a `PersonalInfo` record, then add `Education`, `WorkExperience`, and `Project` entries linked to it.
2. Edit `profileapp/data/personal_facts.yaml` to include Q/A and facts about you.
   - **Q/A format:**
     ```yaml
     qa:
       - q: "What is your full name?"
         a: "Shankar Poudel."
     ```
   - **Facts format:** (converted to Q/A automatically)
     ```yaml
     facts:
       - "I completed an MSc in Computer Science at UNR in 2023."
     ```

## How the Chatbot Works

- Uses `sentence-transformers` (PyTorch backend) to embed your questions and the bot's knowledge.
- Performs cosine similarity to pick the closest answer.
- No remote calls; everything runs locally.
- Edit `profileapp/data/personal_facts.yaml`; restart the server to reload.

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

## Notes

- This is intentionally simple. You can later swap the encoder, add auth, or persist chat history.
- If CUDA is available, the encoder will use it automatically.

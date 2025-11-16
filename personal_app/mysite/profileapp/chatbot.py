import os
import torch
import yaml
from sentence_transformers import SentenceTransformer

# Optionally limit PyTorch CPU threads for your 4-core CPU
torch.set_num_threads(4)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'personal_facts.yaml')
INDEX_PT = os.path.join(os.path.dirname(__file__), 'data', 'facts_index.pt')


class PersonalFactsChatbot:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        # You’re on CPU-only Linux, so we force CPU explicitly for clarity
        self.device = 'cpu'
        self.model = SentenceTransformer(model_name, device=self.device)

        # List of dicts: {'q': ..., 'a': ...}
        self.facts = []
        self.emb = None

        self._load_facts()
        self._build_index()

    def _load_facts(self):
        """
        Load Q/A pairs and facts from personal_facts.yaml.

        Expected YAML format:

        qa:
          - q: "What is your full name?"
            a: "Shankar Poudel."

        facts:
          - "I completed an MSc in Computer Science and Engineering at UNR with a 4.0 GPA."
        """
        if not os.path.exists(DATA_PATH):
            # Fallback if file is missing
            self.facts = [{
                'q': 'who are you',
                'a': 'I am a personal assistant bot. Please add personal_facts.yaml to teach me more.'
            }]
            return

        with open(DATA_PATH, 'r') as f:
            data = yaml.safe_load(f) or {}

        # Q/A pairs
        qa_list = data.get('qa', []) or []
        # Ensure each item is a dict with 'q' and 'a'
        self.facts = [
            {'q': item.get('q', '').strip(), 'a': item.get('a', '').strip()}
            for item in qa_list
            if isinstance(item, dict) and item.get('q') and item.get('a')
        ]

        # Plain facts (no explicit question) – convert to QA
        facts_only = data.get('facts', []) or []
        for fact in facts_only:
            if not fact:
                continue
            # IMPORTANT FIX: single braces {} not {{}} (no set)
            self.facts.append({
                'q': f'fact: {fact}',
                'a': fact
            })

        # If still empty, keep a safe fallback
        if not self.facts:
            self.facts = [{
                'q': 'who are you',
                'a': 'I am a personal assistant bot, but I have no personal facts yet.'
            }]

    def _build_index(self):
        """
        Encode all questions/prompts into an embedding matrix for similarity search.
        """
        texts = [item['q'] for item in self.facts if item.get('q')]
        if not texts:
            self.emb = torch.empty(0)
            return

        with torch.no_grad():
            emb = self.model.encode(
                texts,
                convert_to_tensor=True,
                normalize_embeddings=True
            )
        self.emb = emb

    def respond(self, user_text: str, top_k: int = 3, threshold: float = 0.35) -> str:
        """
        Given a user question, find the closest Q in self.facts by cosine similarity
        and return its answer.

        If similarity is too low, suggest possible topics instead of hallucinating.
        """
        user_text = (user_text or "").strip()
        if not user_text:
            return "Please ask a question about my background, projects, or experience."

        if self.emb is None or self.emb.numel() == 0:
            return (
                "I don't have any personal data yet. "
                "Please add facts in profileapp/data/personal_facts.yaml and reload."
            )

        with torch.no_grad():
            q_emb = self.model.encode(
                [user_text],
                convert_to_tensor=True,
                normalize_embeddings=True
            )[0]
            scores = (self.emb @ q_emb).float()

            best_val, best_idx = torch.max(scores, dim=0)
            best_score = best_val.item()

            if best_score < threshold:
                # Fallback: show a few closest topics instead of pretending to know
                k = min(top_k, len(self.facts))
                top_vals, top_idx = torch.topk(scores, k=k)
                hints = [self.facts[i]['q'] for i in top_idx.tolist()]
                return (
                    "I'm not entirely sure about that. "
                    "Try asking more specifically about my education, work, LLM experience, or projects. "
                    f"(Closest topics I know: { '; '.join(hints) })"
                )

            return self.facts[best_idx.item()]['a']

# Wordle Solver Web App

A responsive, interactive Wordle Utility tool featuring a decoupled Python algorithmic solver backend and a vanilla JavaScript frontend. The application utilizes letter-positional frequency matrices to dynamically evaluate board feedback and calculate the top 3 optimal next word recommendations in real time.

---

## 🚀 Key Features

* **Algorithmic Word Scoring:** Evaluates words based on historical English letter-frequency data mapping across specific string indexes.
* **Smart Filtering:** Tracks multi-turn match histories, successfully capturing grey (absent), yellow (present, wrong spot), and green (correct spot) tiles sequentially without losing state.
* **Stateless Network Architecture:** Communicates over clean JSON payloads via a Flask REST endpoint (`/submit-guess`), passing cumulative move history between frontend UI and the specialized algorithmic module.
* **Decoupled Architecture:** Separates server routing concerns (`app.py`) entirely from tactical word validation logic (`solver.py`).

---

## 📂 Project Structure

```text
ProjectFolder/
│
├── app.py               # Main Flask web server & routing entrypoint
├── solver.py            # Wordle solving algorithms & matrix evaluation
├── 5letterWords.txt     # Local dictionary dataset of valid words
├── requirements.txt     # Lean production-ready dependency specifications
├── .gitignore           # Keeps environment clutter and caches off GitHub
│
├── templates/
│   └── WordleSolver.html # Main game board interface layout
│
└── static/
    ├── app.js           # Handles UI interaction, DOM scraping, and fetch lifecycles
    └── styles.css       # Layout styles matching native Wordle 2D aesthetics

# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight FastAPI + HTML/CSS educational assistant based on the supplied project documentation.

## Features

- Question answering
- Beginner-friendly concept explanations
- Three or more configurable MCQ quiz generation
- Educational passage summarization
- Beginner-to-advanced learning paths
- Interactive quiz answer checking in the browser
- JSON REST API
- Health endpoint
- Optional local LaMini-Flan-T5 explanation provider
- Automated API/module tests

## Project structure

```text
EduGenie/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── gemini_client.py
│   ├── qna.py
│   ├── explanation_module.py
│   ├── quiz_module.py
│   ├── summary_module.py
│   └── learning_path.py
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   ├── test_api.py
│   └── test_modules.py
├── main.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
└── README.md
```

## VS Code setup on Windows

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

```powershell
py -3 -m venv .venv
```

5. Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the server without activation using `.venv\Scripts\python.exe`, or adjust your PowerShell execution policy according to your organization's policy.

6. Upgrade pip and install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Copy `.env.example` to `.env` and put your Gemini API key in `GEMINI_API_KEY`.

## Run

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Optional local explanation model

The original documentation names `LaMini-Flan-T5-783M` for concept explanations. The project keeps that option but does not force a large ML download during the normal setup.

Install:

```powershell
pip install -r requirements-local.txt
```

Then set:

```env
EXPLANATION_PROVIDER=local
```

The first local explanation may download the model from Hugging Face.

## API endpoints

### POST /qa

```json
{"text":"Which is the largest ocean?"}
```

### POST /explain

```json
{"text":"Explain the Pythagorean theorem to a beginner."}
```

### POST /quiz

```json
{"text":"Water boils at 100°C at sea level.","question_count":3}
```

### POST /summarize

```json
{"text":"Paste a long educational passage here."}
```

### POST /learn/recommendations

```json
{"text":"SQL"}
```

### GET /health

Returns:

```json
{"status":"ok","service":"EduGenie"}
```

## Testing

Install the development test runner:

```powershell
pip install pytest
```

Run:

```powershell
pytest -q
```

The tests mock Gemini, so they do not consume API quota.

## Notes

The supplied documentation refers to Gemini 1.5 Pro. This implementation uses Google's current `google-genai` SDK interface and reads the model name from `GEMINI_MODEL`, allowing the deployed model to be changed without changing application code.

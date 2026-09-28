# EduGenie API quick reference

All AI endpoints accept JSON and return a JSON object containing `result`.

| Method | Endpoint | Input |
|---|---|---|
| GET | `/health` | none |
| POST | `/qa` | `{"text":"..."}` |
| POST | `/explain` | `{"text":"..."}` |
| POST | `/quiz` | `{"text":"...","question_count":3}` |
| POST | `/summarize` | `{"text":"..."}` |
| POST | `/learn/recommendations` | `{"text":"..."}` |

FastAPI also generates interactive documentation at `/docs`.

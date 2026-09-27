@echo off
if exist .venv\Scripts\python.exe (
  .venv\Scripts\python.exe -m uvicorn main:app --reload
) else (
  python -m uvicorn main:app --reload
)

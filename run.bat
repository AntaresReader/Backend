@echo off
echo Starting FastAPI Application...
uvicorn app.main:app --reload
pause

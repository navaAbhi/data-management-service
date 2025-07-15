# scripts.ps1
Write-Host "Starting Redis server..."
Start-Process -NoNewWindow -FilePath "redis-server" 

Start-Sleep -Seconds 2

Write-Host "Starting Celery worker..."
Start-Process -NoNewWindow -FilePath "powershell" -ArgumentList "celery -A src.celery_app.celery_app worker --loglevel=info"

Start-Sleep -Seconds 2

Write-Host "Starting FastAPI (Uvicorn)..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

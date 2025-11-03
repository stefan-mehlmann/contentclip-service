# contentclip-service

docker login
docker buildx build --platform linux/amd64,linux/arm64 -t mehlmann/repos:cc-svc --push .

kubectl apply -f k8s-deploy.yml    
kubectl apply -f cloudflare-tunnel.yml  

https://cc-svc.mehlmann.com/docs


# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate

# Dependencies installieren
pip3 install --no-cache-dir -r requirements.txt

# Starten
python3 app.py

# Usage
## Datei hochladen
curl -X POST \
  -F "file1=@data1.xlsx" \
  -F "file2=@data2.xlsx" \
  http://localhost:8000/upload

# Response:
{
  "job_id": "abc-123-def",
  "status": "pending",
  "created_at": "2025-11-02T10:30:00",
  "message": "Files 'data1.xlsx' and 'data2.xlsx' uploaded successfully..."
}

# Swagger UI (interaktiv)
http://localhost:8000/docs

# ReDoc (alternative Darstellung)
http://localhost:8000/redoc

# OpenAPI Schema (JSON)
http://localhost:8000/openapi.json


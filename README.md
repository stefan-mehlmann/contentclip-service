# contentclip-service

docker logindocker buildx build --platform linux/amd64,linux/arm64 -t mehlmann/repos:cc-svc --push .


kubectl apply -f k8s-deploy.yml    

## Test-URLs
https://cc-svc.mehlmann.com/
https://cc-svc.mehlmann.com/docs
https://cc-svc.mehlmann.com/redoc
https://cc-svc.mehlmann.com/openapi.json

## Dateien hochladen
curl -X POST https://cc-svc.mehlmann.com/upload/csv -F "file1=@20250925_Contentklammer_Titeldaten.csv" -F "file2=@20250925_o2p.csv"

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


# Swagger UI (interaktiv)
http://localhost:8000/docs

# ReDoc (alternative Darstellung)
http://localhost:8000/redoc

# OpenAPI Schema (JSON)
http://localhost:8000/openapi.json


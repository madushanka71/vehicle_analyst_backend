# vehicle_analyst_backend

Vehicle analyst application backend.

## To install uv

In Python, uv is a fast, new package manager and project manager 

```cmd
pip install uv
```

## Setting up

```cmd
git clone 'cloning URL'
cd .\vehicle_analyst_backend
uv venv .venv
.venv\Scripts\Activate
uv pip install -e .
crewai install
```

Add .env file to project root folder and add these content
```text
MODEL = gpt-4.1-mini-2025-04-14
OPENAI_API_KEY = Your openAI key
CORS_ORIGINS = http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://192.168.1.20:3000
```

## Run the project

```cmd
uvicorn src.vehicle_analyst_backend.api:app --reload
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

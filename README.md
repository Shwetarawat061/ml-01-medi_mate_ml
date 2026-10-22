# MediMate.ML

MediMate.ML is a heart disease prediction application. It provides a FastAPI prediction service and a Streamlit web interface. A trained model is included in `model_dir/`, and the source dataset is in `dataset/`.

## Requirements

- Python with `pip` (use a Python version compatible with the pinned packages in `requirements.txt`).
- Internet access when installing dependencies.
- The included model file `model_dir/heart_disease_prediction_model.joblib` to serve predictions.
- The included `dataset/heart.csv` if you plan to train the model again.

## Setup (Windows PowerShell)

Run these commands from the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item env_template.txt .env
```

Edit `.env` and set `PROJECT_ROOT` to the absolute path of this repository. For example:

```dotenv
PROJECT_ROOT=D:/projects/ml-01-medi_mate_ml
```

Keep the other values from `env_template.txt` unless you intentionally want to change the dataset, model, logging, or API paths. The frontend uses `API_URL` to contact the backend; its default is `http://127.0.0.1:8000/predict-heart-disease`.

If PowerShell blocks virtual environment activation, allow scripts for the current terminal session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the application

Start the backend from the repository root in the first terminal:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --reload
```

Start the Streamlit interface from the repository root in a second terminal:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run frontend/app.py
```

Open the local Streamlit URL printed in the second terminal (usually `http://localhost:8501`). Keep the backend running while using the interface.

## API endpoints

- `GET http://127.0.0.1:8000/health` — check that the API is running.
- `POST http://127.0.0.1:8000/predict-heart-disease` — get a prediction. The request body must contain `age`, `sex`, `cp`, `trestbps`, `chol`, `fbs`, `restecg`, `thalach`, `exang`, `oldpeak`, `slope`, `ca`, and `thal`.
- `http://127.0.0.1:8000/docs` — interactive API documentation.

Example request using `curl.exe` in PowerShell:

```powershell
curl.exe -X POST http://127.0.0.1:8000/predict-heart-disease `
  -H "Content-Type: application/json" `
  -d '{"age":52,"sex":1,"cp":0,"trestbps":125,"chol":212,"fbs":0,"restecg":1,"thalach":168,"exang":0,"oldpeak":1.0,"slope":2,"ca":0,"thal":2}'
```

The response includes a binary prediction, a probability, and a diagnosis label. This is a machine learning output, not a medical diagnosis.

## Retrain the model

From the repository root, with the virtual environment active and `.env` configured, run:

```powershell
python -m backend.training
```

Training reads the dataset and settings from `.env`, then writes the resulting model to the configured model path and logs to the configured log directory. Stop and restart the API after retraining so it loads the newly saved model.

## Project layout

```text
backend/       FastAPI service, prediction, and training code
frontend/      Streamlit user interface
dataset/       Training dataset
model_dir/     Pre-trained model used by the API
notebook_files/Exploratory/model development notebook
requirements.txt
               Pinned Python dependencies
env_template.txt
               Environment variable template
```

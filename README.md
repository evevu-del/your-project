# Streamlit Assignment Setup

For this assignment, use a Python virtual environment named `.venv`. Install packages and run Streamlit from that environment.

## Create the virtual environment

```bash
python -m venv .venv
```

If `python` isn’t available on your system, use `python3 -m venv .venv`.

## Activate it

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

## Install the required packages

```bash
pip install streamlit requests
```

## Add them to `requirements.txt`

```
streamlit
requests
```

## Run your app from the same virtual environment

```bash
streamlit run app.py
```

## Streamlit config + secrets

Create `.streamlit/secrets.toml` and add your Hugging Face token:

```toml
HF_TOKEN = "paste_your_hugging_face_token_here"
```

Create `.streamlit/config.toml` for theme/configuration (example):

```toml
[theme]
base = "dark"
primaryColor = "#ef4444"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#f8fafc"
font = "Helvetica"
```

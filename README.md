# NIOTA Housing Intelligence — Flagship Demo

A clean, modern Streamlit demo showing how NIOTA Labs can transform housing application and house lot allocation data into regional decision intelligence for Guyana.

## What this demo shows

- Executive housing KPIs
- A stylized Guyana regional map with Regions 1–10
- Region names visible directly on the map
- Color views for allocations, approval rate, backlog, processing speed, and allocation rate
- Region 4 deep dive
- Ask NIOTA executive questions
- Management brief
- Synthetic demo data only

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Render settings

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

Recommended environment variable:

```text
PYTHON_VERSION=3.11.9
```

## Note

The dataset is fictional and created for demonstration only. It is not official housing data and should not be used for policy claims.

# Zeno Static Site Deployer

This repository contains a simple Django + React application that lets you
upload a ZIP archive containing a static website and then serves the extracted
files from a local folder. The goal is to provide an end‑to‑end demo with a
friendly UI and minimal dependencies.

## Features

* REST API (`POST /api/deploy/`) accepts a ZIP file and returns a JSON object
  with the URL of the deployed site.
* Uploaded archives are unzipped on the server, flattened if they contain a
  single top‑level directory, and copied to `backend/zeno_backend/sites/<id>`.
* Static content is served by Django during development from `/sites/<id>/…`.
* React front end (`forntend/zeno-frontend`) provides drag‑and‑drop file upload,
  progress bar, error handling, and shows the deployment URL.
* CORS is enabled for development and no external storage service is required.

## Running the project

### Backend

```bash
cd backend/zeno_backend
source ../../venv/bin/activate     # adjust path if different
pip install -r requirements.txt    # install dependencies
python manage.py migrate           # create sqlite database
python manage.py runserver         # start development server
```

By default the API is available at `http://127.0.0.1:8000/api/deploy/` and the
sites will be accessible under `http://127.0.0.1:8000/sites/<id>/`.

### Frontend

```bash
cd forntend/zeno-frontend
npm install
npm start                         # opens http://localhost:3000/
```

Upload a ZIP file (e.g. a folder containing `index.html` and assets), click
Deploy, and the returned link should load your static site in a new tab.

To create a production build:

```bash
npm run build   # output is in forntend/zeno-frontend/build/
```


## Deployments & Extensions

* The `deploy/storage.py` module can be adapted to use S3/MinIO or another
  blob store instead of the local `sites/` directory.
* In production you would serve the generated `build/` content via nginx or a
  CDN, and run Django under Gunicorn/Uvicorn.

## Troubleshooting

* If you see `(.venv)` in your prompt, the virtual environment is active; run
  `deactivate` to exit.
* Backend errors appear in the log printed by `manage.py runserver`.
* CORS is enabled for all origins in settings; adjust `CORS_ALLOW_ALL_ORIGINS`
  to narrow it down.

Enjoy deploying static sites with a click!
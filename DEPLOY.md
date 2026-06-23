# Pubblicare il sito red-team su Render (con password)

Web Service Flask che serve il sito dietro HTTP Basic Auth. Protegge sia la
pagina sia gli audio. La password si imposta su Render, non nel codice.

## 1. Prepara la cartella

Copia il contenuto del sito generato dentro `site/`:

```bash
cp -R ~/Downloads/VoiceRedTeam_GiulIA/results/site_<STAMP>/* ~/Downloads/render_app/site/
# deve risultare: render_app/site/index.html  e  render_app/site/audio/...
```

## 2. Prova in locale

```bash
cd ~/Downloads/render_app
pip install -r requirements.txt
BASIC_AUTH_USER=insiel BASIC_AUTH_PASSWORD=scegli-una-password python3 app.py
# apri http://localhost:8000  ->  il browser deve chiedere utente e password
```

## 3. Metti su GitHub

```bash
cd ~/Downloads/render_app
git init && git add -A && git commit -m "Red-team GiulIA - sito protetto"
# crea un repo su GitHub e fai push (gh repo create ... --push, o da web)
```

## 4. Crea il Web Service su Render

- Render -> New + -> **Web Service** -> collega il repo.
- Runtime: Python. Build: `pip install -r requirements.txt`.
  Start: `gunicorn app:app --bind 0.0.0.0:$PORT`  (gia' in render.yaml).
- In **Environment** aggiungi due variabili:
  - `BASIC_AUTH_USER`  = es. `insiel`
  - `BASIC_AUTH_PASSWORD` = la password che sceglierai (segreta)
- Create -> attendi il deploy -> ottieni l'URL `https://redteam-giulia.onrender.com`.

Manda a Insiel: URL + utente + password (su canali separati).

## 5. Aggiornare con il secondo batch

Rigenera/aggiorna `site/`, poi:

```bash
cd ~/Downloads/render_app
git add -A && git commit -m "aggiungo batch 2" && git push
```

Render ridistribuisce da solo.

## Note
- Render free: il servizio va in sleep dopo inattivita' e si risveglia in ~30s
  alla prima richiesta. Per un uso piu' reattivo serve il piano a pagamento.
- La password protegge anche i file audio (tutto passa dal server). Su HTTPS
  (fornito da Render) il Basic Auth e' adeguato per condividere con Insiel.

# Sales Research Pipeline (Google Calendar & AEO Integration)

An automated sales intelligence and briefing pipeline. It queries your Google Calendar for upcoming meetings, retrieves background data about the invitee's company, synthesizes a detailed briefing using Gemini AI, and appends a private Google Doc link directly to the calendar event.

## 📐 Architecture
- **Trigger:** Terminal invocation via on-demand CLI command.
- **Meeting Fetch:** Google Calendar API fetches the next upcoming event.
- **Domain Extraction:** Parses invitee domain (excluding common generic domains like `gmail.com`).
- **OSINT Enrichment:**
  - **Firecrawl API:** Scrapes the company homepage for value propositions, positioning, and context.
  - **You.com Search API:** Gathers recent news, mentions, launches, and funding updates.
- **Synthesis:** Gemini API generates a clean briefing document (Accenture-style corporate voice).
- **Delivery:**
  - Saves a local `.md` file in `prospects/` for local searchability.
  - Generates a Google Doc via Google Docs API.
  - Appends the document link to the Google Calendar description.

## 🛠️ Installation

1. Clone or sync this repository.
2. Initialize virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file:
   ```env
   FIRECRAWL_API_KEY=fc-xxxxxxxxxxxxxxxx
   YOU_API_KEY=ydc-sk-xxxxxxxxxxxxxxxx
   GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxx
   ```
4. Authenticate with Google APIs:
   - Go to Google Cloud Console.
   - Create an OAuth 2.0 Client ID for a **Desktop Application**.
   - Download the client secrets file, rename it to `credentials.json`, and place it in the root of this project folder.

## 🚀 Usage

Simply run:
```bash
python run_research.py
```
- On the first run, a browser tab will open for OAuth authorization. Log in using your Google Account to generate `token.json`.
- Subsequent runs will reuse the credentials silently.

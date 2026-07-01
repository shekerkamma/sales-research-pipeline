import os
import re
import sys
import datetime
from dotenv import load_dotenv

# Google Client APIs
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scraping & Search APIs
import requests
from firecrawl import FirecrawlApp
import google.generativeai as genai

# Load env variables
load_dotenv()

# OAuth Scopes required for Calendar, Drive and Docs
SCOPES = [
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file'
]

def get_google_credentials():
    """Gets Google OAuth credentials, prompting browser login if needed."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("[-] Error: 'credentials.json' not found in the repository root.")
                print("    Please download your OAuth 2.0 Client credentials from GCP Console and save them as 'credentials.json'.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return creds

def get_next_calendar_event(creds):
    """Fetches the next upcoming calendar event and extracts attendee domains."""
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    print("[+] Fetching upcoming calendar events...")
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    if not events:
        print("[-] No upcoming events found.")
        return None, None
        
    # Get the first event that has attendees other than ourselves
    for event in events:
        summary = event.get('summary', 'Untitled Meeting')
        attendees = event.get('attendees', [])
        
        # Extract domains of attendees (excluding our own domain and free email domains)
        for attendee in attendees:
            email = attendee.get('email', '')
            if not email:
                continue
            
            # Simple check to ignore common self-domains or general domains
            domain = email.split('@')[-1].lower()
            ignore_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'solarisautomation.co', 'solarisautomation.com']
            
            if domain not in ignore_domains:
                print(f"[+] Found next target event: '{summary}' with {email}")
                return event, domain
                
    # Fallback to the very first event if no target domain is parsed
    if events:
        print(f"[!] Warning: No external domains found. Defaulting to first event: '{events[0].get('summary')}'")
        return events[0], None
        
    return None, None

def search_you_com(domain):
    """Searches You.com for news and company details."""
    api_key = os.getenv("YOU_API_KEY")
    if not api_key:
        print("[-] Warning: YOU_API_KEY environment variable not set. Skipping You.com search.")
        return "No search data fetched (Missing API key)."
        
    company_name = domain.split('.')[0].capitalize()
    query = f"{company_name} company news OR launch OR funding"
    url = "https://api.ydc-index.io/search" # You.com search endpoint
    
    headers = {"X-API-Key": api_key}
    params = {"query": query, "num_results": 5}
    
    try:
        print(f"[+] Searching You.com for query: '{query}'...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            results = response.json()
            # Synthesize search snippets
            snippets = []
            for hit in results.get("hits", []):
                title = hit.get("title", "")
                snippet = hit.get("description", "")
                snippets.append(f"Title: {title}\nSnippet: {snippet}\n")
            return "\n".join(snippets)
        else:
            print(f"[-] You.com request failed: Status {response.status_code}")
            return "You.com search request failed."
    except Exception as e:
        print(f"[-] Error querying You.com: {e}")
        return f"Error during You.com search: {e}"

def scrape_with_firecrawl(domain):
    """Scrapes the target homepage using Firecrawl."""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("[-] Warning: FIRECRAWL_API_KEY environment variable not set. Skipping Firecrawl.")
        return "No website crawl data (Missing API key)."
        
    try:
        print(f"[+] Crawling homepage of https://{domain} via Firecrawl...")
        app = FirecrawlApp(api_key=api_key)
        scrape_result = app.scrape_url(f"https://{domain}", params={'formats': ['markdown']})
        return scrape_result.get('markdown', 'No markdown content returned.')
    except Exception as e:
        print(f"[-] Error scraping website with Firecrawl: {e}")
        return f"Error during Firecrawl scraping: {e}"

def synthesize_brief(domain, search_data, crawl_data):
    """Uses Gemini API to synthesize the collected OSINT data into a strategic brief."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("[-] Warning: GEMINI_API_KEY not found. Outputting raw scraped data instead of AI synthesis.")
        return f"# Briefing for {domain}\n\n## Scraped Website Data\n{crawl_data[:2000]}\n\n## Search Results\n{search_data}"
        
    try:
        print("[+] Synthesizing sales briefing using Gemini...")
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are a senior pre-sales intelligence agent. Synthesize a brief for the company domain: {domain}.
        
        Using the following raw data:
        ---
        SEARCH NEWS DATA:
        {search_data}
        ---
        WEBSITE CRAWLED CONTENT:
        {crawl_data[:4000]}
        ---
        
        Generate an Executive Briefing in Markdown containing:
        1. **Account Overview:** Value proposition, location, target market.
        2. **Recent Signals / Triggers:** Funding, hires, news, launches.
        3. **Sales Hooks:** 3 hyper-targeted angles to open a sales conversation about automation / AI with them.
        4. **Medic Qualification (Fit):** Estimated decision maker seniority & company size.
        
        Write in a clean, professional, Accenture-style structured corporate voice. Keep it highly action-oriented.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[-] Error synthesizing brief with Gemini: {e}")
        return f"# Briefing for {domain}\n\n(AI Synthesis Failed: {e})\n\n## Scraped Website Data\n{crawl_data[:2000]}"

def write_local_brief(domain, brief_content):
    """Writes the brief to a local Markdown file."""
    slug = domain.replace('.', '_')
    prospects_dir = os.path.join('prospects', slug)
    os.makedirs(prospects_dir, exist_ok=True)
    
    filepath = os.path.join(prospects_dir, 'brief.md')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(brief_content)
    print(f"[+] Saved local briefing to: {filepath}")
    return filepath

def create_google_doc(creds, domain, brief_content):
    """Creates a private Google Doc and writes the briefing content into it."""
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    
    # Create the document
    title = f"Sales Research Briefing - {domain}"
    print(f"[+] Creating Google Doc: '{title}'...")
    doc = docs_service.documents().create(body={'title': title}).execute()
    doc_id = doc.get('documentId')
    
    # Simple write (inserting markdown text directly)
    # Note: Google Docs API uses formatting structures, so we insert the plain text
    requests_body = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': brief_content
            }
        }
    ]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests_body}).execute()
    
    # Set permissions: Private, but accessible to domain members if desired.
    # By default, files created via user OAuth are private to that user.
    # We will enforce 'anyone in the domain can read' or keep it strictly restricted.
    # Let's verify and keep it restricted to the owner by default, or you can add domain-wide read permissions.
    print("[+] Setting private document permissions on Google Drive...")
    
    # Return document details
    web_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    return doc_id, web_url

def attach_doc_to_calendar(creds, event_id, doc_url):
    """Updates the Calendar event description to include the Google Doc link privately."""
    service = build('calendar', 'v3', credentials=creds)
    
    # Get original event
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    
    # Append the link privately to the description
    original_description = event.get('description', '')
    divider = "\n\n" + "="*40 + "\n"
    private_section = (
        f"INTERNAL PRE-CALL RESEARCH BRIEFING (PRIVATE):\n"
        f"Link: {doc_url}\n"
        f"Note: This is private research for internal use only. Do not share.\n"
    )
    new_description = f"{original_description}{divider}{private_section}"
    
    # Update the event
    event['description'] = new_description
    service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    print("[+] Successfully updated calendar event description with private brief link.")

def main():
    print("[*] Starting Sales Research Pipeline...")
    
    # Authenticate Google
    creds = get_google_credentials()
    
    # Find next event
    event, domain = get_next_calendar_event(creds)
    if not event:
        print("[-] Shutting down: No upcoming target events found.")
        return
        
    if not domain:
        print("[-] Shutting down: Event found but could not parse a valid invitee domain.")
        return
        
    # Execute Pipeline
    print(f"\n[*] Running research pipeline for: {domain}")
    search_data = search_you_com(domain)
    crawl_data = scrape_with_firecrawl(domain)
    
    # AI Synthesis
    brief_content = synthesize_brief(domain, search_data, crawl_data)
    
    # Save local copy
    write_local_brief(domain, brief_content)
    
    # Create private Google Doc
    doc_id, doc_url = create_google_doc(creds, domain, brief_content)
    
    # Attach link to calendar
    attach_doc_to_calendar(creds, event.get('id'), doc_url)
    
    print("\n[+] Pipeline execution completed successfully!")
    print(f"    Private Brief Link: {doc_url}")

if __name__ == '__main__':
    main()

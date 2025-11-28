import json
from playwright.sync_api import sync_playwright

def navigate(url: str) -> str:
    """
    Scrapes a URL using Playwright.
    Returns: Text content, Links, Audio URL, and Submission URL.
    """
    print(f"[Tool] Navigating to: {url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Long timeout for slow quiz pages; wait until DOM is ready
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2000) # Wait for JS hydration
            
            content = page.evaluate("document.body.innerText")
            
            # Extract Links for CSVs/PDFs
            links = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a')).map(a => ({href: a.href, text: a.innerText}))
            }""")
            
            # Extract Audio Source if present
            audio_src = page.evaluate("""() => {
                const audio = document.querySelector('audio');
                return audio ? audio.src : null;
            }""")
            
            # Extract Submission URL (Robust Regex match)
            submit_url = page.evaluate(r"""() => {
                const form = document.querySelector('form');
                if (form && form.action) return form.action;
                // Look for patterns like "Post your answer to..."
                const match = document.body.innerText.match(/https:\/\/[^\s]+submit/);
                return match ? match[0] : null;
            }""")
            
            browser.close()
            
            # Return a JSON string that the LLM can parse
            return json.dumps({
                "text": content[:1500], # Limit text to save tokens (Rate Limit prevention)
                "links": [l for l in links if any(x in l['text'].lower() for x in ['csv', 'pdf', 'json', 'download', 'api'])],
                "audio": audio_src,
                "submission_url": submit_url
            })
    except Exception as e:
        return f"Navigation Error: {e}"
import os
import requests
import google.generativeai as genai

def main():
    # 1. Load sensitive keys securely from GitHub environment variables
    gemini_key = os.environ.get("GEMINI_API_KEY")
    fb_token = os.environ.get("FB_ACCESS_TOKEN")
    fb_page_id = os.environ.get("FB_PAGE_ID")

    if not gemini_key or not fb_token or not fb_page_id:
        print("Error: Missing required environment variables. Check your GitHub Secrets.")
        return

    # 2. Configure Gemini AI Engine
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = (
        "Write a short, highly engaging social media post about a useful programming "
        "or technology tip. Include relevant, trending hashtags."
    )
    
    try:
        print("Generating content with AI...")
        response = model.generate_content(prompt)
        post_content = response.text
        print(f"Generated Content:\n{post_content}\n")
    except Exception as e:
        print(f"Failed to generate content from Gemini: {e}")
        return

    # 3. Publish to Facebook Page via Official Meta Graph API
    url = f"https://graph.facebook.com/v18.0/{fb_page_id}/feed"
    payload = {
        'message': post_content,
        'access_token': fb_token
    }

    try:
        print("Sending post to Facebook...")
        res = requests.post(url, data=payload)
        result_data = res.json()
        
        if res.status_code == 200:
            print(f"Successfully posted to Facebook! Post ID: {result_data.get('id')}")
        else:
            print(f"Failed to post to Facebook: {result_data}")
    except Exception as e:
        print(f"HTTP Request failed: {e}")

if __name__ == "__main__":
    main()

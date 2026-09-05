import os
import requests
from google import genai

def main():
    # ১. গিটহাব সিক্রেট থেকে ভেরিয়েবলগুলো লোড করা
    gemini_key = os.environ.get("GEMINI_API_KEY")
    fb_token = os.environ.get("FB_ACCESS_TOKEN")
    fb_page_id = os.environ.get("FB_PAGE_ID")

    # সিক্রেট ঠিকমতো দেওয়া আছে কিনা তা চেক করা
    if not gemini_key or not fb_token or not fb_page_id:
        print("Error: Missing required environment variables. Check your GitHub Secrets.")
        return

    # ২. লেটেস্ট জেমিনি ক্লায়েন্ট কনফিগারেশন
    client = genai.Client(api_key=gemini_key)
    
    prompt = (
        "Write a short, highly engaging social media post about a useful programming "
        "or technology tip. Include relevant, trending hashtags."
    )
    
    try:
        print("Generating content with AI...")
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
        )
        post_content = response.text
        print(f"Generated Content:\n{post_content}\n")
    except Exception as e:
        print(f"Failed to generate content from Gemini: {e}")
        return

    # ৩. অফিসিয়াল মেটা গ্রাফ এপিআই (Meta Graph API) এর মাধ্যমে ফেসবুক পেজে পোস্ট পাঠানো
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

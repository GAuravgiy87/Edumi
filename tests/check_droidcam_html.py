"""Check what DroidCam returns"""
import requests

url = "http://192.168.29.220:4747/video"
response = requests.get(url, timeout=5)

print("DroidCam /video response:")
print("=" * 60)
print(response.text[:1000])  # First 1000 chars
print("=" * 60)

# Look for video URLs in the HTML
if 'video' in response.text.lower() or 'mjpeg' in response.text.lower():
    print("\nFound video-related content in HTML")
    # Extract potential video URLs
    import re
    urls = re.findall(r'(\/[a-zA-Z0-9_\/\.]+)', response.text)
    print("Potential paths found:")
    for u in set(urls):
        if 'video' in u.lower() or 'mjpeg' in u.lower() or 'feed' in u.lower():
            print(f"  {u}")

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def get_video_url_from_api(insta_url):
    api_url = "https://insta-reels-downloader-the-fastest-hd-reels-fetcher-api.p.rapidapi.com/unified/index"
    querystring = {"url": insta_url}
    
    headers = {
        "x-rapidapi-host": "insta-reels-downloader-the-fastest-hd-reels-fetcher-api.p.rapidapi.com",
        "x-rapidapi-key": "afd51ede22msh92dc70853f30068p179ecdjsn56e9275092b0" 
    }

    try:
        response = requests.get(api_url, headers=headers, params=querystring)
        json_data = response.json()
        
        media_type = json_data.get('media_type')
        
        # Smart routing based on post type
        if media_type == 'video':
            return json_data.get('data', {}).get('content', {}).get('media_url')
            
        elif media_type == 'sidecar':
            items = json_data.get('data', {}).get('content', {}).get('items', [])
            for item in items:
                if item.get('type') == 'video':
                    return item.get('media_url')
                    
        return None
        
    except Exception as e:
        print(f"Extraction Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"success": False, "error": "No URL provided."})
        
    download_url = get_video_url_from_api(url)
    
    if download_url:
        return jsonify({"success": True, "download_url": download_url})
    else:
        return jsonify({"success": False, "error": "Target video not found in payload."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

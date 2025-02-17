from flask import Flask, render_template
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

NASA_API_KEY = "c1P1OVFnGuP1KrgizeBOgIYZcSeS6l7W7sgsNIPK"
BASE_URL = "https://api.nasa.gov/planetary/apod"

@app.route('/')
def index():
    # Get the last 10 days of NASA photos
    photos = []
    today = datetime.now()

    for i in range(10):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        params = {
            "api_key": NASA_API_KEY,
            "date": date
        }

        try:
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                #only include images (some days might be videos)
                if data["media_type"] == "image":
                    photos.append({
                        'title': data['title'],
                        'date': data['date'],
                        'url': data['url'],
                        'explanation': data['explanation']
                    })
        except requests.RequestException as e:
                print(f"Error fetching data for date {date}: {e}")
                continue
        
    return render_template('index.html', photos=photos)

# Create templates directory and index.html file
if not os.path.exists('templates'):
    os.makedirs('templates')

with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NASA Photo Gallery</title>
    <style>
            body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f0f0;
            }
            .photo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
            }
            .photo-card {
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
            }
            .photo-card:hover {
            transform: translateY(-5px);
            }
            .photo-card img {
            width: 100%;
            height: 400px;
            object-fit: cover;
            }
            .photo-info {
            padding: 15px;
            }
            .photo-title h2 {
            font-size: 1.2em;
            margin: 0 0 10px 0;
            color: #333;
            }
            .photo-date {
            color: #777;
            font-size: 0.9em;
            }
            .photo-explanation {
            margin-top: 15px;
            font-size: 0.95em;
            color: #555;
            height: 25em;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: visible;
            }
        </style>
</head>
<body>
    <h1>NASA Photo Gallery</h1>
    <div class="photo-grid">
        {% for photo in photos %}
        <div class="photo-card">
            <img src="{{ photo.url }}" alt="{{ photo.title }}">
            <div class="photo-info">
                <div class="photo-title"><h2>{{ photo.title }}</h2></div>
                <div class="photo-date">{{ photo.date }}</div>
                <div class="photo-explanation">{{ photo.explanation }}</div>    
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)

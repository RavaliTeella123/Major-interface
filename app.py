from flask import Flask, render_template, request, redirect, url_for
from gtts import gTTS
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['VOICES_FOLDER'] = os.path.join('static', 'voices')
app.config['CAPTIONS_FILE'] = os.path.join('static', 'captions.txt')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_caption(image_filename):
    with open(app.config['CAPTIONS_FILE'], 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if parts[0] == image_filename:
                return parts[1]
    return "Caption not found"

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    
    image = request.files['image']
    
    if image.filename == '' or not allowed_file(image.filename):
        return redirect(url_for('index'))
    
    # Save the image
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)
    
    # Get caption for the image
    caption = get_caption(image.filename)
    
    # Generate voice for the caption
    if not os.path.exists(app.config['VOICES_FOLDER']):
        os.makedirs(app.config['VOICES_FOLDER'])

    voice_path = os.path.join(app.config['VOICES_FOLDER'], 'caption.mp3')

    tts = gTTS(text=caption, lang='en')
    tts.save(voice_path)
    
    return render_template('result.html', image_path=image_path, voice_path=voice_path, caption=caption)

if __name__ == '__main__':
    app.run(debug=True)

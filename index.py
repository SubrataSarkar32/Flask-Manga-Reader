# index.py
from flask import Flask, render_template, abort, redirect, url_for
import os
import cv2

app = Flask(__name__,
    static_url_path='',
    static_folder='.')

@app.route('/')
def home():
    chapters = []
    videos = []
    for file in sorted(os.listdir('.')):
        directory = './' + file
        if os.path.isdir(directory):
            for filename in sorted(os.listdir(directory)):
                if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".gif") or filename.endswith(".webp"):
                    chapters.append((file, os.path.join(directory.replace('#', '%23'), filename), file.replace('#', '%23')))
                    break
                elif filename.endswith(".mp4"):
                    if not os.path.isfile(os.path.join(directory, "zimage.jpg")):
                        cap = cv2.VideoCapture(os.path.join(directory, filename))
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 5)
                        ret, frame = cap.read()
                        cv2.imwrite(os.path.join(directory, "zimage.jpg"), frame)
                    videos.append((file, os.path.join(directory.replace('#', '%23'), "zimage.jpg"), file.replace('#', '%23')))
                    break
    return render_template('home.html', chps=chapters, vids=videos)

@app.route('/search/')
def searchNone():
    return redirect('/')

@app.route('/search/<query>')
def search(query):
    chapters = []
    videos = []
    for file in os.listdir('.'):
        directory = file
        if os.path.isdir(directory) and query in file:
            for filename in sorted(os.listdir(directory)):
                if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".gif") or filename.endswith(".webp"):
                    chapters.append((file, os.path.join(directory.replace('#', '%23'), filename), file.replace('#', '%23')))
                    break
                elif filename.endswith(".mp4"):
                    videos.append((file, os.path.join(directory.replace('#', '%23'), "image.jpg.kv"), file.replace('#', '%23')))
                    break
    return render_template('search.html', chps=chapters, vids=videos, qry=query)

@app.route('/<chapter_name>')
def read(chapter_name):
    images = []
    videos = []
    for filename in os.listdir('./' + chapter_name):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".gif") or filename.endswith(".webp"):
            images.append(os.path.join(chapter_name.replace('#', '%23'), filename))
        elif filename.endswith(".mp4"):
            videos.append(os.path.join(chapter_name.replace('#', '%23'), filename))
    
    if len(images) > 0:
        try:
            images = sorted(images, key=lambda x: int(x.split("/")[-1].split(".")[0]))
        except Exception as e:
           images = sorted(images)
    if len(videos) > 0:
        videos = sorted(videos)

    total_pages = len(images)
    if total_pages == 0:
        total_pages = 1  # fallback

    page_index = 0
    return render_template('read.html', txt=chapter_name, imgs=images, vids=videos, total_pages=total_pages, page_index=page_index, show_all_images=True)

@app.route('/read/page/<chapter_name>/<int:page_index>')
def read_page(chapter_name, page_index):
    chapter_path = './' + chapter_name
    if not os.path.exists(chapter_path):
        abort(404)

    images = []
    videos = []
    for filename in os.listdir(chapter_path):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".gif") or filename.endswith(".webp"):
            images.append(os.path.join(chapter_name.replace('#', '%23'), filename))  # No replace here
        elif filename.endswith(".mp4"):
            videos.append(os.path.join(chapter_name.replace('#', '%23'), filename))

    if len(images) > 0:
        try:
            images = sorted(images, key=lambda x: int(x.split("/")[-1].split(".")[0]))
        except Exception as e:
            images = sorted(images)

    total_pages = len(images)
    if total_pages == 0:
        abort(404)

    if page_index < 0 or page_index >= total_pages:
        abort(404)

    selected_image = images[page_index]
    return render_template('read.html', txt=chapter_name, imgs=images, vids=videos, total_pages=total_pages, page_index=page_index, selected_image=selected_image, show_all_images=False)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')

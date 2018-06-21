from flask import Flask, render_template, abort
import os.path
app = Flask(__name__,
    static_url_path='',
    static_folder='.')

@app.route('/')
def home():
    chapters = []
    for file in os.listdir('.'):
        directory = './' + file
        if os.path.isdir(directory):
            for filename in os.listdir(directory):
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    chapters.append((file, directory.replace('#', '%23') + '/' + filename, file.replace('#', '%23')))
                    break
    return render_template('home.html', chps = chapters)

@app.route('/<chapter_name>')
def read(chapter_name):
    images = []
    for filename in os.listdir('./' + chapter_name):
        if filename.endswith(".png") or filename.endswith(".jpg"): 
            images.append('./' + chapter_name.replace('#', '%23') + '/' + filename)
    if len(images) > 0:
        return render_template('read.html', imgs = images)

if __name__ == '__main__':
    app.run(debug=True)

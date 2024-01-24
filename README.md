# Flask Manga Reader

A Python Flask application that lets you navigate and read downloaded manga using your browser.

![Alt text](assets/example.png?raw=true)

### Prerequisites

```bash
# Install Python 3
brew install python
# Install Flask
pip install -r requirements.txt
```

### Instructions

1. Move files from Flask-Manga-Reader into your manga directory
```
-| Flask-Manga-Reader
 |-- assets
 |-- new_folder1
 |-- new_folder2
 ...
```
2. `flask --app wsgi` to start the application
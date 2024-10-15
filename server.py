from flask import Flask, render_template
from threading import Thread

app = Flask('')


@app.route('/')
def home():
  return """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Online website</title>
    <style>
        div {
            display: flex;
            box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.5);
            color: rgb(255, 255, 255);
            margin: 0 auto;
            background-color: #f0cece;
            text-align: center;
            width: 500px;
            height: 200px;
            border-radius: 10px;
            justify-content: center;
            align-items: center;
        }
        
        body {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            height: 100vh;
        }
    </style>
</head>
<body>
    <div class="1d">
        <h1>Your Bot is Online!!</h1>
    </div>
</body>
</html>"""


def index():
  return render_template("index.html")


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()

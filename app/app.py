from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "O iubesc pe Ema"


if __name__ == "__main__":
    app.run(debug=True)
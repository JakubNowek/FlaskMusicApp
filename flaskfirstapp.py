# set FLASK_APP=flaskfirstapp.py - pozwala na uruchamianie serwera komendą: flask run
# set FLASK_DEBUG=1 - pozwala na tryb debugowania. Dzięki temu jeśli coś zmenię i zapiszę zmiany to nie muszę
# restartować serwera, żeby je zobaczyć - tak samo działa jak się napisze na dole w app.run(debug=True) ale to działa
# w uruchamianiu w pythonie - py flaskfirstapp.py
# ustawianie zmiennych środowiskowych działa tylko w danej sesji terminala
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return "<h1>Homo page</h1>"


@app.route('/about')
def about():
    return "<h1 style='color:red'>About page</h1>"


if __name__ == '__main__':
    app.run(debug=True)

# set FLASK_APP=flaskfirstapp.py - pozwala na uruchamianie serwera komendą: flask run
# set FLASK_DEBUG=1 - pozwala na tryb debugowania. Dzięki temu jeśli coś zmenię i zapiszę zmiany to nie muszę
# restartować serwera, żeby je zobaczyć - tak samo działa jak się napisze na dole w app.run(debug=True) ale to działa
# w uruchamianiu w pythonie - py flaskfirstapp.py
# ustawianie zmiennych środowiskowych działa tylko w danej sesji terminala
from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
# dummy data, which pretends a database response with posts
posts = [
    {
        'author': 'Tomasz Strzelba',
        'title': 'Blog Post 1',
        'content': 'First post content - here i would place some description of the page functionalities or whatever',
        'date': 'November 2, 2022'
    },
    {
        'author': 'Katarzyna Katastrofa',
        'title': 'Blog Post 2',
        'content': 'Second post content - it may be just another html site',
        'date': 'November 4, 2022'
    }
]


class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Prześlij')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename))
                  )  # Then save the file
        flash('Przesłano plik')
        return redirect(url_for('index'))# "File has been uploaded."
    return render_template('home.html', posts=posts, form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)

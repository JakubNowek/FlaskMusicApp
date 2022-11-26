# set FLASK_APP=flaskfirstapp.py - pozwala na uruchamianie serwera komendą: flask run
# set FLASK_DEBUG=1 - pozwala na tryb debugowania. Dzięki temu jeśli coś zmenię i zapiszę zmiany to nie muszę
# restartować serwera, żeby je zobaczyć - tak samo działa jak się napisze na dole w app.run(debug=True) ale to działa
# w uruchamianiu w pythonie - py flaskfirstapp.py
# ustawianie zmiennych środowiskowych działa tylko w danej sesji terminala
from flask import Flask, render_template, url_for, redirect, flash, session, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import os
import process_sound
from process_sound import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

filter_list = [f for f in dir(process_sound) if(
                                                f[0] != '_' and
                                                f not in ['os', 'func'])
               ]

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


class SelectFilterForm(FlaskForm):
    filter = SelectField('Wybierz filtr', choices=filter_list)#choices=[('LP', 'LowPass'), ('HP', 'HighPass'), ('Cut', 'Cut')])
    submit = SubmitField('Użyj')


@app.route('/', methods=['GET', 'POST'])
def index():
    ufform = UploadFileForm()
    sfform = SelectFilterForm()
    if ufform.validate_on_submit():
        file = ufform.file.data  # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename))
                  )  # Then save the file
        session['input_filename'] = file.filename
        #flash(f'Przesłano plik {test_function(session["name"])}')  # displaying filename
        flash(f'Przesłano plik {session["input_filename"]}')  # displaying filename
        #test_function(session["input_filename"])
        return redirect(url_for('index'))
    if sfform.validate_on_submit():  # co się dzieje po kliknięciu akceptacji filtra
        session['choice_filter'] = sfform.filter.data
        return redirect(url_for('sound_processing'))
    return render_template('home.html', posts=posts, ufform=ufform, sfform=sfform, name=session.get('name'))


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/sound_processing')
def sound_processing():
    filename = session["input_filename"]
    if filename[-4:] == '.txt':
        func(getattr(process_sound, session['choice_filter']), filename)
    return redirect(url_for('download_file'))


@app.route('/download')
def download_file():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        app.config['UPLOAD_FOLDER'],
                        session["input_filename"])
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

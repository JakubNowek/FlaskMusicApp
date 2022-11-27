# set FLASK_APP=flaskfirstapp.py - pozwala na uruchamianie serwera komendą: flask run
# set FLASK_DEBUG=1 - pozwala na tryb debugowania. Dzięki temu jeśli coś zmenię i zapiszę zmiany to nie muszę
# restartować serwera, żeby je zobaczyć - tak samo działa jak się napisze na dole w app.run(debug=True) ale to działa
# w uruchamianiu w pythonie - py flaskfirstapp.py
# ustawianie zmiennych środowiskowych działa tylko w danej sesji terminala
from flask import Flask, render_template, url_for, redirect, flash, session, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField, FloatField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, DataRequired
import os
import process_sound
from process_sound import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

filter_list = [f for f in dir(process_sound) if(f[0] != '_' and
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


# class SelectFilterForm(FlaskForm):
#     filter = SelectField('Wybierz filtr', choices=filter_list)#choices=[('LP', 'LowPass'), ('HP', 'HighPass'), ('Cut', 'Cut')])
#     param1 = SelectField('Wybierz filtr', choices=[('op1', 'opcja1'), ('op2', 'opcja2'), ('op3', 'opcja3')])
#     submit = SubmitField('Użyj')


class EchoFilterForm(FlaskForm):
    delay = FloatField(description='Opóźnienie [s]', validators=[DataRequired()])
    decay = FloatField(description='Wyciszenie (0-1)', validators=[DataRequired()])
    submit = SubmitField('Zastosuj')


class AmpFilterForm(FlaskForm):
    amp = FloatField(description='Wzmocnienie [0-100%]', validators=[DataRequired()])
    submit = SubmitField('Zastosuj')


@app.route('/', methods=['GET', 'POST'])
def index():
    ufform = UploadFileForm()
    # sfform = SelectFilterForm()
    echoform = EchoFilterForm()
    ampform = AmpFilterForm()
    if len(os.listdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER']))) == 0:
        session['input_filename'] = None
    if ufform.validate_on_submit():  # wybor pliku
        file = ufform.file.data  # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename))
                  )  # Then save the file
        session['input_filename'] = file.filename
        flash(f'Przesłano plik {session["input_filename"]}')  # displaying filename
        return redirect(url_for('index'))

    # if sfform.validate_on_submit():  # co się dzieje po kliknięciu akceptacji filtra z rozwijanej listy
    #     session['choice_filter'] = sfform.filter.data
    #     return redirect(url_for('sound_processing'))

    if echoform.validate_on_submit():  # po wpisaniu echa
        session['choice_filter'] = 'echo'
        session['echo'] = {'delay': echoform.delay.data,
                           'decay': echoform.decay.data}
        return redirect(url_for('sound_processing'))

    if ampform.validate_on_submit():  # po wpisaniu wzmocnienia
        session['choice_filter'] = 'amp'
        session['amp'] = ampform.amp.data
        return redirect(url_for('sound_processing'))

    return render_template('home.html', posts=posts, ufform=ufform, name=session.get('name'),
                           # sfform=sfform,
                           echoform=echoform,
                           ampform=ampform,
                           filename=session['input_filename']
                           )


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/sound_processing')
def sound_processing():
    filename = session["input_filename"]
    if filename == None:
        flash('Nie przesłano pliku', category="error")  # wiadomość o braku pliku
        return redirect(url_for('index'))
    data = session[session['choice_filter']]
    if filename[-4:] == '.txt':  # tymczasowa walidacja rozszerzenia pliku
        func(getattr(process_sound, session['choice_filter']), filename, data)
    return redirect(url_for('download_file'))


@app.route('/download')
def download_file():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        app.config['UPLOAD_FOLDER'],
                        session["input_filename"])
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

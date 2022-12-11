# set FLASK_APP=flaskfirstapp.py - pozwala na uruchamianie serwera komendą: flask run
# set FLASK_DEBUG=1 - pozwala na tryb debugowania. Dzięki temu jeśli coś zmenię i zapiszę zmiany to nie muszę
# restartować serwera, żeby je zobaczyć - tak samo działa jak się napisze na dole w app.run(debug=True) ale to działa
# w uruchamianiu w pythonie - py flaskfirstapp.py
# ustawianie zmiennych środowiskowych działa tylko w danej sesji terminala
from flask import Flask, render_template, url_for, redirect, flash, session, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField, FloatField, IntegerField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, DataRequired, ValidationError
import os
import process_sound
from process_sound import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = r'static\files'

# deleting files if the update folder is not empty (better option would be to delete at the end
# and allowing only one filw with max size)
if len(app.config['UPLOAD_FOLDER']) != 0:
    for fil in os.scandir(app.config['UPLOAD_FOLDER']):
        os.remove(fil.path)


class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])
    submit = SubmitField('Prześlij')


class EchoFilterForm(FlaskForm):
    delay = FloatField(description='Opóźnienie [s]', validators=[DataRequired()])
    decay = FloatField(description='Wyciszenie (0-1)', validators=[DataRequired()])
    submit = SubmitField('Zastosuj')


class AmpFilterForm(FlaskForm):
    amp = FloatField(description='Wzmocnienie [0-100%]', validators=[DataRequired()])
    submit = SubmitField('Zastosuj')


class RevFilterForm(FlaskForm):
    submit = SubmitField('Odwróć')


class LPFilterForm(FlaskForm):
    cut_off_l = FloatField(description='Wzmocnienie [0-100%]', validators=[DataRequired()])
    submit = SubmitField('Zastosuj')


class HPFilterForm(FlaskForm):
    cut_off_h = FloatField(description='Wzmocnienie [0-100%]', validators=[DataRequired()])
    submit = SubmitField('Zastosuj')


class RepeatFilterForm(FlaskForm):
    n_times = IntegerField(description='Wzmocnienie [0-100%]', validators=[DataRequired()])
    submit = SubmitField('Zastosuj')


@app.route('/', methods=['GET', 'POST'])
def index():
    ufform = UploadFileForm()
    # Filtry
    echoform = EchoFilterForm()
    ampform = AmpFilterForm()
    revform = RevFilterForm()
    lpform = LPFilterForm()
    hpform = HPFilterForm()
    repform = RepeatFilterForm()

    if len(os.listdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER']))) == 0:
        session['input_filename'] = None
    if ufform.validate_on_submit():  # wybor pliku
        file = ufform.file.data  # First grab the file
        if file.filename[-4:] != '.wav':
            flash('Brak poprawnego pliku', category="error")  # wiadomość o braku pliku
            session['input_filename'] = None
            return redirect(url_for('index'))
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename))
                  )  # Then save the file
        session['input_filename'] = " ".join(file.filename.split()).replace(" ", "_")
        session['filepath'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                           app.config['UPLOAD_FOLDER'],
                                           secure_filename(file.filename))

        flash(f'Przesłano plik {file.filename}')  # displaying filename
        return redirect(url_for('index'))

    if echoform.validate_on_submit():  # po wpisaniu echa
        session['choice_filter'] = 'echo'
        session['echo'] = {'delay': echoform.delay.data,
                           'decay': echoform.decay.data}
        return redirect(url_for('sound_processing'))

    if ampform.validate_on_submit():  # po wpisaniu wzmocnienia
        session['choice_filter'] = 'amp'
        session['amp'] = ampform.amp.data
        return redirect(url_for('sound_processing'))

    if lpform.validate_on_submit():  # po wpisaniu czestoftliwosci low
        session['choice_filter'] = 'low_pass'
        session['low_pass'] = lpform.cut_off_l.data
        return redirect(url_for('sound_processing'))

    if hpform.validate_on_submit():  # po wpisaniu czestoftliwosci high
        session['choice_filter'] = 'high_pass'
        session['high_pass'] = hpform.cut_off_h.data
        return redirect(url_for('sound_processing'))

    if repform.validate_on_submit():  # po wpisaniu czestoftliwosci high
        session['choice_filter'] = 'repeat'
        session['repeat'] = repform.n_times.data
        return redirect(url_for('sound_processing'))

    if revform.validate_on_submit():  # po kliknięciu odwrócenia
        session['choice_filter'] = 'rev'
        session['rev'] = 500
        return redirect(url_for('sound_processing'))



    return render_template('home.html', ufform=ufform, name=session.get('name'),
                           echoform=echoform,
                           ampform=ampform,
                           revform=revform,
                           lpform=lpform,
                           hpform=hpform,
                           repform=repform,
                           filename=session['input_filename']
                           )


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/sound_processing')
def sound_processing():
    filename = session["input_filename"]
    filepath = session["filepath"]
    if filename == None:
        flash('Brak poprawnego pliku', category="error")  # wiadomość o braku pliku
        return redirect(url_for('index'))
    data = session[session['choice_filter']]
    if filename[-4:] == '.wav':  # tymczasowa walidacja rozszerzenia pliku
        func(getattr(process_sound, session['choice_filter']), filepath, data)
    return redirect(url_for('download_file'))


@app.route('/download')
def download_file():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        app.config['UPLOAD_FOLDER'],
                        session["input_filename"])
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)


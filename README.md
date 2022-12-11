# Uruchomienie programu

###Aby uruchomić program, należy:

- pobrać folder FlaskMusicApp
- w folderze utworzyć wirtualne środowisko (zalecane)
- zainstalować framework Flask
- pobrać pobrać zaimportowane w skryptach pakiety Pythona
  - z plików 'process_sound.py' oraz 'flaskfirstapp.py'
  
- ustawić zmienne środowiskowe
- uruchomić aplikację

###Tworzenie i uruchamianie wirtualnego środowiska dla Pythona 3:
$ python3  -m venv venv
####Uruchamianie _venv_ w Linux/macOS:
$ source venv/bin/activate
####Uruchamianie _venv_ w Windows:
$ venv\Scripts\activate
###Instalowanie Flask:
$ pip install flask
###Ustawianie zmiennych środowiskowych:
####Linux / macOS:
$ export FLASK_APP=flaskfirstapp.py
####Windows:
$ set FLASK_APP=flaskfirstapp.py

###Uruchamianie aplikacji:
$ flask run



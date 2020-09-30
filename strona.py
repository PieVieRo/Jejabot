from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
	stronka = """
	komendy:<br>
	j!strzałki - pokazuje strzałki<br>
	j!avek - pokazuje avek<br>
	j!pd - pokazuje pd <br>
	j!link - daje link do profilu
	"""
	return stronka

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()
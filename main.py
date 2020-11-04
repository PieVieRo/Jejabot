# discord :OOO
import discord
from discord.ext import commands

# jakies gowno wazne i niewazne
from os import getenv

# do brania info
from lxml import html
import requests

# baza danych zeby zarejestrowac sb
from replit import db

from error import BadUserError

# chce zeby bot za free dzialal
from strona import keep_alive
keep_alive()

# opis
description = "bot dla jejaków"

# database:

#  ___________________________________
# |                    |              |
# | uzytkownik discord | nick na jeja |
# |____________________|______________|


# bot
bot = commands.Bot(command_prefix='j!')

class Uzytkownik():
	def __init__(self, user: str):
		self.link = "https://www.jeja.pl/user,{}".format(user)
		jeja = requests.get(self.link)
		strona = html.fromstring(jeja.content)
		
		# nazwa użytkownika
		self.nick = strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[1]/div[2]/text()')[0]

		# zdjęcie profilowe
		self.avek = strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/img/@src')[0]

		# poziom doświadczenia
		self.lvl = strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[3]/div[2]/div[2]/div[1]/strong/text()')[0]

		# liczba punktów doświadczenia
		self.pkt = strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[3]/div[2]/div[2]/div[2]/strong/text()')[0]

		# ilość strzałek w górę
		self.strzalki = strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[5]/div[2]/div[1]/text()')[0]

# better class
class Temp():
	def __init__(self, user: str):
		self.link = "https://www.jeja.pl/user,{}".format(user)
		jeja = requests.get(self.link)
		self._strona = html.fromstring(jeja.content)

		check = self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/h2/text()')[0]

		if check == "Informacja":
			raise BadUserError(f"Nie ma użytkownika o nazwie `{user}`")

		dane_left = self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[@class="profil-dane"]/div[@class="profil-dane-left"]/text()')

		if "Strona www:" in dane_left:
			dane_left.remove("Strona www:")

		dane_right = self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[@class="profil-dane"]/div[@class="profil-dane-right"]/text()')

		self.dane = {k[:-1]:v for k,v in zip(dane_left,dane_right)}

		self.pd = self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[@class="profil liczby-one liczby-one-two"]/div/strong/text()')

		if not self.pd:
			self.brakpd = True

		self.raw_staty = self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[@class="profil-liczby"]/div')



	# zwraca link do profilu
	def get_link(self):
		return self.link

	# zwraca opis profilu
	def get_opis(self):
		opis = self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[@class="profil-opis"]/div[2]/text()')
		if opis:
			return opis[0]

	# zwraca avatar profilu
	def get_avatar(self):
		pass
	
	# zwraca ilość strzałek
	def get_strzalki(self):
		hasStrzalki = "Komentarze" in self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[@class="profil-liczby"]/div[@class="profil-liczby-left"]/text()')
		strzalki = self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[5]/div[@class="profil-liczby-right"]/div[@class="bn"]/text()')
		return strzalki[0] if hasStrzalki else None

	# zwraca login uzytkownika
	def get_login(self):
		return self.dane["Login"]


# jeśli bot dołączy
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# wysyła ilość strzałek w górę
@bot.command()
async def strzalki(ctx, user: str):
	try:
		
		uzytkownik = Uzytkownik(user)
		await ctx.send(f"{uzytkownik.nick} ma `{uzytkownik.strzalki}` strzałek w górę")
	except:
		await ctx.send(f"Nie ma użytkownika o nazwie `{user}`")

@bot.command()
async def pd(ctx, user: str):
	try:
		uzytkownik = Uzytkownik(user)
		await ctx.send(f"{uzytkownik.nick} ma poziom `{uzytkownik.lvl}` i `{uzytkownik.pkt}` punktów doświadczenia")
	except:
		await ctx.send(f"Nie ma użytkownika o nazwie `{user}`")

@bot.command()
async def avek(ctx, user: str):
	try:
		uzytkownik = Uzytkownik(user)
		await ctx.send(f"Zdjęcie profilowe użytkownika {uzytkownik.nick}")
		await ctx.send(uzytkownik.avek)
	except:
		await ctx.send(f"Nie ma użytkownika o nazwie `{user}`")

@bot.command(aliases=['profil'])
async def link(ctx, user: str):
	try:
		uzytkownik = Uzytkownik(user)
		await ctx.send(f"link do profilu: {uzytkownik.link}")
	except:
		await ctx.send(f"Nie ma użytkownika o nazwie `{user}`")

@bot.command()
async def test_link(ctx, user: str):
	try:
		uzytkownik = Temp(user)
	except BadUserError as e:
		await ctx.send(e)
		return
	await ctx.send(uzytkownik.get_link())

@bot.command()
async def test_strzalki(ctx, user: str):
	try:
		uzytkownik = Temp(user)
	except BadUserError as e:
		await ctx.send(e)
		return
	strzalki = uzytkownik.get_strzalki()

	if strzalki is not None:
		await ctx.send(f"{uzytkownik.get_login()} ma `{strzalki}` strzałek w górę")
	else:
		await ctx.send(f"{uzytkownik.get_login()} ma ukryte strzałki albo ich po prostu nie ma")

@bot.command()
async def ranking(ctx):
	ranking = []
	do_wyslania = ''
	with ctx.typing():
		for i in range(4):
			znaczki = f"https://www.jeja.pl/doswiadczenie,miesiac,{i}"
			strona = requests.get(znaczki)
			wszystko = html.fromstring(strona.content)
			ranking.extend(wszystko.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[@class="best-month-box"]/div/div[1]/a/text()'))
		for k,v in enumerate(ranking):
			do_wyslania += f"{k+1}. {v}\n"
	await ctx.send(f"Ranking w tym miesiącu\n```{do_wyslania}```")
	await ctx.send(len(ranking))

@bot.command()
async def dev(ctx, user: str):
	try:
		uzytkownik = Temp(user)
	except BadUserError as e:
		await ctx.send(e)
		return
	await ctx.send(uzytkownik.raw_staty)

# dziala bot
bot.run(getenv('token'))

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

# better class
# gonna change Uzytkownik() to this soon
class Uzytkownik():
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

	# zwraca link do profilu
	# returns link to profile
	def get_link(self):
		return self.link

	# zwraca opis profilu
	# return profile's description
	def get_opis(self):
		opis = self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[@class="profil-opis"]/div[2]/text()')
		if opis:
			return opis[0]

	# zwraca avatar profilu
	# returns profile picture
	def get_avatar(self):
		avek = self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/img/@src')
		return avek[0]
	
	# zwraca ilość strzałek
	# returns upvote count
	def get_strzalki(self):
		hasStrzalki = "Komentarze" in self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[@class="profil-liczby"]/div[@class="profil-liczby-left"]/text()')
		strzalki = self._strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[5]/div[@class="profil-liczby-right"]/div[@class="bn"]/text()')
		return strzalki[0] if hasStrzalki else None

	# zwraca login uzytkownika
	# returns username
	def get_login(self):
		return self.dane["Login"]


# jeśli bot dołączy
# when bot starts
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print(discord.__version__)
	print('------')

# wysyła link do profilu
# sends profile link
@bot.command(aliases=['profil'])
async def link(ctx, user: str):
	try:
		uzytkownik = Uzytkownik(user)
	except BadUserError as e:
		await ctx.send(e)
		return
	await ctx.send(uzytkownik.get_link())

# wysyła ilość strzałek w górę
# sends upvotes count
@bot.command(alias=['strzałki'])
async def strzalki(ctx, user: str):
	try:
		uzytkownik = Uzytkownik(user)
	except BadUserError as e:
		await ctx.send(e)
		return
	strzalki = uzytkownik.get_strzalki()

	if strzalki is not None:
		await ctx.send(f"{uzytkownik.get_login()} ma `{strzalki}` strzałek w górę")
	else:
		await ctx.send(f"{uzytkownik.get_login()} ma ukryte strzałki albo ich po prostu nie ma")

# wysyła obrazek profilowy użytkownika
# sends user's profile picture
@bot.command()
async def avek(ctx, user: str):
	try:
		uzytkownik = Uzytkownik(user)
	except BadUserError as e:
		await ctx.send(e) 
		return
	
	await ctx.send(f"Profil użytkownika {uzytkownik.get_login()}")
	await ctx.send(uzytkownik.get_avatar())
	
# pokazuje ranking memiarzy (nie miesięczny)
# shows ranking
@bot.command()
async def ranking(ctx):
	ranking = []
	do_wyslania = ''
	async with ctx.typing():
		for i in range(5):
			znaczki = f"https://memy.jeja.pl/ranking_memiarzy,{i}"
			strona = requests.get(znaczki)
			wszystko = html.fromstring(strona.content)
			ranking.extend(wszystko.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div/div/div/div[1]/a/text()'))
		for k,v in enumerate(ranking):
			do_wyslania += f"{k+1}. {v}\n"
	await ctx.send(f"Ranking w tym miesiącu\n```{do_wyslania}```")

# dziala bot
bot.run(getenv('token'))

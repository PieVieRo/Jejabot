class BadUserError(Exception):
	def __init__(self, user: str):
		self.message(f"Nie ma użytkownika o nazwie `{user}`")
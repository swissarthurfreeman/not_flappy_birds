#############################################################
# Auteur: Arthur Freeman                   Date: 20/02/2019 #
# Programme: Unit qui accède à la base de données qui       #
# contient les scores de Not Flappy Birds                   #
# Basé sur: https://www.youtube.com/watch?v=vISRn5qFrkM     #
#############################################################
import gspread #gspread et oauth2client doivent être installés via pip isntalll.
from oauth2client.service_account import ServiceAccountCredentials
class scoresObject:
	def __init__(self, scope):
		self.scope = scope
		self.creds = ServiceAccountCredentials.from_json_keyfile_name('scores.json', self.scope)
		self.client = gspread.authorize(self.creds)
		self.sheet = self.client.open('scores_database').sheet1
		self.listOfLists = self.sheet.get_all_records()
	def sort(self):
		self.listOfLists.sort(key = lambda x:x['score'], reverse = True)

def loadScores():
	global scoresVar
	scoresVar = scoresObject(['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
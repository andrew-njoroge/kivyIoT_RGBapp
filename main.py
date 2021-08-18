import kivy
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from  kivy.uix.button import Button
import pyrebase
import json
import requests

kezz = []
class SignupWindow(Screen):
	userr = ObjectProperty(None)
	passwordi = ObjectProperty(None)
	
	
	#waka = "AIzaSyAso8HtWVAyLxTyqyj52TMO3GThdNfFXJg"  #web api key
	firebaseconfig = {
		"apiKey": "AIzaSyAso8HtWVAyLxTyqyj52TMO3GThdNfFXJg",
		"authDomain": "rgb-led-project.firebaseapp.com",
		"databaseURL": "https://rgb-led-project-default-rtdb.europe-west1.firebasedatabase.app",
		"projectId": "rgb-led-project",
		"storageBucket": "rgb-led-project.appspot.com",
		"messagingSenderId": "448826405701",
		"appId": "1:448826405701:web:d14e1f9732ff6ccb5e842c",
		"measurementId": "G-SBNKDMF10D"
		}
	firebase = pyrebase.initialize_app(firebaseconfig)
	auth = firebase.auth()
	db = firebase.database()


	def sign_up(self):
		email = self.userr.text
		password = self.passwordi.text
		print(email,password)
		try:
			user = self.auth.create_user_with_email_and_password(email, password)
			self.ids.signup_erra_message.text =  "User Created Successfully"
		except requests.exceptions.HTTPError as error :
			#print(error)
			error_message = json.loads(error.args[1])['error']['message']
			#print(error_message)
			self.ids.signup_erra_message.text =  error_message
			


class LoginWindow(SignupWindow):
	wifiname = ObjectProperty(None)
	#wifipassword = ObjectProperty(None)
	
	def login(self):
		email = self.userr.text
		password = self.passwordi.text
		wifiname1 = self.wifiname.text
		#wifipass1 = self.wifipassword.text
		 
		kezz.insert(1,wifiname1) #UserWifiSSID 
		#kezz.insert(2,wifipass1) #UserWifiPassword
		kezz.insert(0,password) #to get the path token down in the main window class
		#print(email,password)

		try:
			login = self.auth.sign_in_with_email_and_password(email, password)
			self.ids.signup_erra_message1.text="Successfully logged in!"
			
		except requests.exceptions.HTTPError as error1:
			#print(error1)
			error1_message = json.loads(error1.args[1])['error']['message']
			#print(error1_message)
			if error1_message == "EMAIL_NOT_FOUND":
				self.ids.signup_erra_message1.text= error1_message + "Press signup button"
			else:
				self.ids.signup_erra_message1.text= error1_message


	

class MainWindow(LoginWindow):
	red = ObjectProperty(0.5)
	green = ObjectProperty(0.5)
	blue = ObjectProperty(0.5)
	#firebase_url = 'https://rgb-led-project-default-rtdb.europe-west1.firebasedatabase.app/.json'

	def printout(self):
		redder = format(self.red.value , ".3f" )
		greener = format(self.green.value , ".3f" ) 
		bluer = format(self.blue.value , ".3f" )
		#print("e", "'"+kezz[0]+"'")
		kramby = "'"+kezz[0]+"'"
		
		#res = isinstance(bluer, str)  #the entities above are already strings
		#print("Red:", redder,  "Green:", greener ,"Blue:", bluer  )
		redde = float(redder) * 255
		greenie = float(greener) * 255
		bluebol = float(bluer) * 255
		#print(redde,greenie,bluebol)

		
		json_data = {"red" : redde , "green" : greenie , "blue": bluebol, "SSID" : kezz[1]}
		self.db.child(kramby).set(json_data)
		#res = requests.put(url = self.firebase_url , json = json_data)
		#print (res)

class WindowManager(ScreenManager):
	pass


elixir = Builder.load_file('rgbslider.kv')

#print(format(432.456, ".2f"))
class Multiple_Slider(App):
	def build(self):
		return elixir

if __name__ == '__main__':
	Multiple_Slider().run()
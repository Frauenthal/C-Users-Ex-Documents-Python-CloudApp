#Change to environmental variables later

class Config:
	SECRET_KEY ='00397d11a11b7a115ab75203b455ea2d'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

	#mail setup These values are specific to using gmail
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True

	#Refrence M2M "environment"
	MAIL_USERNAME = 'TicketManagerPlusNU@gmail.com'
	MAIL_PASSWORD = 'TMPCode!!55'
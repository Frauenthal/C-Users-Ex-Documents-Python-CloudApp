#to run page
#cd C:\Users\Ex\Documents\Python\CloudApp
#set FLASK_APP=run.py
#set FLASK_DEBUG=1
#python -m flask run

#or 

#cd C:\Users\Ex\Documents\Python\CloudApp
#python run.py

#Can be viewed at
#http://localhost:5000/


from FlaskPage import create_app

#configuration can be added to creat_app to run configuration
app = create_app()

#allows app to be run easily from python
if __name__ == '__main__':
	app.run(debug=True)
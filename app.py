#Import flask
#Import render template to return html templates.
#Import json to display it
#Import request to do HTTP requests
#Import mysql to use it
#Import password salter
from flask import Flask, render_template, json, request, redirect, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'Bahaha'

#Configure MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Magic331'
app.config['MYSQL_DATABASE_DB'] = 'bucketlist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#Define the basic route and request handler
@app.route("/")
def main():
	return render_template('index.html')

#Define signup route
@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

#Define signup method
@app.route('/signUp', methods=['POST'])
def signUp():
	#Create user

	#Read values from UI
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']

	#Salt password
	_hashed_password = generate_password_hash(_password)

	#Create connection and cursor to query
	conn = mysql.connect()
	cursor = conn.cursor()

	#Call stored procedure
	cursor.callproc('sp_createUser', (_name, _email, _hashed_password))

	#Feth and commit if it works
	data = cursor.fetchall()
	if len(data) is 0:
		conn.commit()
		return json.dumps({'message':'User created successfully!'})
	else:
		return json.dumps({'error': str(data[0])})

	#Validate values
	if _name and _email and _password:
		return json.dumps({'html':'<span>All fields good!</span>'})
	else:
		return json.dumps({'html':'<span>Enter the required fields.</span>'})

#Signin route
@app.route('/showSignIn')
def showSignin():
	return render_template('signin.html')

#Validate
@app.route('/validateLogin', methods=['POST'])
def validateLogin():
	#Try to read input
	try:
		_username = request.form['inputEmail']
		_password = request.form['inputPassword']

		args = []
		args.append(_username)

		#Create a mysql connection and validate
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_validateLogin', args)

		#Get fetched records
		data = cursor.fetchall()
		if len(data) > 0:
			if check_password_hash(str(data[0][3]), _password):
				# Store the session
				session['user'] = data[0][0]
				return redirect('/userHome')
			else:
				return render_template('error.html', error = 'Wrong email address or password.')
		else:
			return render_template('error.html', error = 'Wrong email address or password.')
	except Exception as e:
		return render_template('error.html', error = str(e))
	finally:
		cursor.close()
		conn.close()

#User route
@app.route('/userHome')
def userHome():
	#If we have a user, show it. Otherwise show unauthorized
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('error.html', error = 'Unauthorized access.')

#Logout
@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect('/')

#Add wish
@app.route('/showAddWish')
def showAddWish():
	return render_template('addWish.html')

@app.route('/addWish', methods=['POST'])
def addWish():
	#Add wish

	try:
		if session.get('user'):
			#Get info and check session
			_title = request.form['inputTitle']
			_description = request.form['inputDescription']
			_user = session.get('user')

			#Create connection and add wish
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_addWish', (_title, _description, _user))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return redirect('/userHome')
			else:
				return render_template('error.html', error = 'An error occured.')
		else:
			return render_template('error.html', error = 'Unauthorized access.')
	except Exception as e:
		return render_template('error.html', error = str(e))
	finally:
		cursor.close()
		conn.close()

#Get wishes
@app.route('/getWish')
def getWish():
	try:
		if session.get('user'):
			_user = session.get('user')

			#Connect to mysql and fetch
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_getWishByUser', (_user,))
			wishes = cursor.fetchall()

			#Once we've fetched data, convert to a dictionary so that it's easy to return json.
			wishes_dict = []
			for wish in wishes:
				wish_dict = {
					'Id': wish[0],
					'Title': wish[1],
					'Description': wish[2],
					'Date': wish[3]
				}
				wishes_dict.append(wish_dict)

			return json.dumps(wishes_dict)
		else:
			return render_template('error.html', error = 'Unauthorized access.')
	except Exception as e:
		return render_template('error.html', error = str(e))

#Check if executed file is the main program and run the app
if __name__ == "__main__":
	app.debug = True
	app.run()
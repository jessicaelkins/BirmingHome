import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField,SubmitField,BooleanField,DateTimeField,RadioField,SelectField,TextField,TextAreaField)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired

app = Flask (__name__)
Bootstrap(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRAC_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'oursecretkey'

db = SQLAlchemy(app)
Migrate(app,db)

class FilterForm (FlaskForm):
    location1 = BooleanField ("Downtown")
    location2 = BooleanField ("Hoover")
    location3 = BooleanField ("Meadowbrook")
    location4 = BooleanField ("Homewood")
    location5 = BooleanField ("Vestavia")
    location6 = BooleanField ("Other")
    type1 = BooleanField ("Plumbing")
    type2 = BooleanField ("Cleaning")
    type3 = BooleanField ("Pet")
    type4 = BooleanField ("Yardwork")
    type5 = BooleanField ("Painting")
    type6 = BooleanField ("Heating/Cooling")
    type7 = BooleanField ("Electrical")
    type8 = BooleanField ("Other")
    filter=SubmitField("Filter")

class EditForm (FlaskForm):
    profilePic = StringField ('Profile Picture (http links only):')
    phoneNumber = StringField ('Phone Number:')
    aboutMe = TextAreaField()
    submit = SubmitField('Confirm')

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    firstName = db.Column(db.Text)
    lastName = db.Column(db.Text)
    email = db.Column(db.Text, unique = True)
    password = db.Column(db.Text)

    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

    def __repr__(self):
        return f"{self.firstName} {self.lastName} {self.email} {self.password}"

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.Text)
    email = db.Column(db.Text)
    titleOfJob = db.Column(db.Text)
    typeOfJob = db.Column(db.Text)
    locationOfJob = db.Column(db.Text)
    descOfJob = db.Column(db.Text)

    def __init__(self, fullname, email, titleOfJob, typeOfJob, locationOfJob, descOfJob):
        self.fullname = fullname
        self.email = email
        self.titleOfJob = titleOfJob
        self.typeOfJob = typeOfJob
        self.locationOfJob = locationOfJob
        self.descOfJob = descOfJob

    def __repr__(self):
        return f"{self.fullname} {self.email} {self.titleOfJob} {self.typeOfJob} {self.locationOfJob} {self.descOfJob}"

class Profile(db.Model):
    __tablename__="profiles"

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.Text)
    profilePic = db.Column(db.Text)
    phoneNumber = db.Column(db.Text)
    aboutMe = db.Column(db.Text)

    def __init__(self, email, profilePic, phoneNumber, aboutMe):
        self.email = email
        self.profilePic = profilePic
        self.phoneNumber = phoneNumber
        self.aboutMe = aboutMe

    def __repr__(self):
        return f"{self.email} {self.profilePic} {self.phoneNumber} {self.aboutMe}"

db.create_all()

@app.route('/', methods = ['GET', 'POST'])
def index ():
    noUser = False
    notMatch = False

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        searchUsers = User.query.filter(User.email == email).all()

        if searchUsers:
            getUser = searchUsers[0]
            getPassword = getUser.password

            if getPassword == password:
                session['email'] = email
                return redirect('homepage')
            else:
                notMatch = True
        else:
            noUser = True
    return render_template('index.html', noUser=noUser, notMatch=notMatch)

@app.route('/signup', methods = ['GET', 'POST'])
def signup ():

    notMatch = False
    alreadyUser = False
    passed = True
    trueOrFalse = [False, False, False, False]
    requirements = ["You did not use an uppercase letter", "You did not use a lowercase letter", "You did not end your password with a number", "Your password was not 8 or more characters long"]

    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        checkEmail = User.query.filter(User.email == email).all()

        if password == confirmPassword and not checkEmail:
            length = len(password)

            for x in password:
                if x.isupper():
                    trueOrFalse[0] = True
                    break

            for x in password:
                if x.islower():
                    trueOrFalse[1] = True
                    break

            if password[length-1].isnumeric():
                trueOrFalse[2] = True

            if length >= 8:
                trueOrFalse[3] = True

            if all(trueOrFalse):
                passed = True
                newUser = User (firstName, lastName, email, password)
                db.session.add(newUser)
                db.session.commit()

                newProfile = Profile (email, "", "", "")
                db.session.add(newProfile)
                db.session.commit()
                return redirect('thankyou')
            else:
                passed = False

        if password != confirmPassword:
            notMatch = True

        if checkEmail:
            alreadyUser = True

    return render_template('signup.html', notMatch=notMatch, alreadyUser=alreadyUser, trueOrFalse=trueOrFalse, requirements=requirements, passed=passed, enu=enumerate(trueOrFalse))

@app.route('/homepage', methods = ['GET', 'POST'])
def homepage ():
    email = session.get('email', None)
    searchUsers = User.query.filter(User.email == email).all()
    getUser = searchUsers[0]
    firstName = getUser.firstName
    lastName = getUser.lastName
    fullName = firstName + " " + lastName

    typeOne, typeTwo, typeThree, typeFour, typeFive, typeSix, typeSeven, typeEight = "[]", "[]", "[]", "[]", "[]", "[]", "[]", "[]"
    locationOne, locationTwo, locationThree, locationFour, locationFive, locationSix = "[]", "[]", "[]", "[]", "[]", "[]"
    location_one, location_two, location_three, location_four, location_five, location_six = False, False, False, False, False, False
    type_one, type_two, type_three, type_four, type_five, type_six, type_seven, type_eight = False, False, False, False, False, False, False, False
    location1, location2, location3, location4, location5, location6 = False, False, False, False, False, False
    type1, type2, type3, type4, type5, type6, type7, type8 = False, False, False, False, False, False, False, False
    noneSelected = True

    form = FilterForm()

    if form.validate_on_submit():
        location1 = form.location1.data
        location2 = form.location2.data
        location3 = form.location3.data
        location4 = form.location4.data
        location5 = form.location5.data
        location6 = form.location6.data
        type1 = form.type1.data
        type2 = form.type2.data
        type3 = form.type3.data
        type4 = form.type4.data
        type5 = form.type5.data
        type6 = form.type6.data
        type7 = form.type7.data
        type8 = form.type8.data
        noneSelected = False

        if location1:
            location_one = True
            locationOne = Post.query.filter(Post.locationOfJob == "downtown").all()

        if location2:
            location_two = True
            locationTwo = Post.query.filter(Post.locationOfJob == "hoover").all()

        if location3:
            location_three = True
            locationThree = Post.query.filter(Post.locationOfJob == "meadowbrook").all()

        if location4:
            location_four = True
            locationFour = Post.query.filter(Post.locationOfJob == "homewood").all()

        if location5:
            location_five = True
            locationFive = Post.query.filter(Post.locationOfJob == "vestavia").all()

        if location6:
            location_six = True
            locationSix = Post.query.filter(Post.locationOfJob == "other").all()

        if type1:
            type_one = True
            typeOne = Post.query.filter(Post.typeOfJob == "plumbing").all()

        if type2:
            type_two = True
            typeTwo = Post.query.filter(Post.typeOfJob == "cleaning").all()

        if type3:
            type_three = True
            typeThree = Post.query.filter(Post.typeOfJob == "pet").all()

        if type4:
            type_four = True
            typeFour = Post.query.filter(Post.typeOfJob == "yardwork").all()

        if type5:
            type_five = True
            typeFive = Post.query.filter(Post.typeOfJob == "painting").all()

        if type6:
            type_six = True
            typeSix = Post.query.filter(Post.typeOfJob == "heating/cooling").all()

        if type7:
            type_seven = True
            typeSeven = Post.query.filter(Post.typeOfJob == "electrical").all()

        if type8:
            type_eight = True
            typeEight = Post.query.filter(Post.typeOfJob == "other").all()

        if location1 + location2 + location3 + location4 + location5 + location6 == False:
            if type1 + type2 + type3 + type4 + type5 + type6 + type7 + type8 == False:
                noneSelected = True

    elif request.method == 'POST':
        title = request.form['title']
        type = request.form['type']
        location = request.form['location']
        description = request.form['description']

        newPost = Post (fullName, email, title, type, location, description)
        db.session.add(newPost)
        db.session.commit()

    all_posts = Post.query.all()
    if location1 + location2 + location3 + location4 + location5 + location6 == False:
        if type1 + type2 + type3 + type4 + type5 + type6 + type7 + type8 == False:
            noneSelected = True
    return render_template('homepage.html', email=email, all_posts=all_posts, form=form, type_one=type_one, type_two=type_two, type_three=type_three, type_four=type_four, type_five=type_five,
                            type_six=type_six, type_seven=type_seven, type_eight=type_eight, location_one=location_one, location_two=location_two, location_three=location_three,
                            location_four=location_four, location_five=location_five, locaton_six=location_six, typeOne=typeOne, typeTwo=typeTwo, typeThree=typeThree, typeFour=typeFour,
                            typeFive=typeFive, typeSix=typeSix, typeSeven=typeSeven, typeEight=typeEight, locationOne=locationOne, locationTwo=locationTwo, locationThree=locationThree,
                            locationFour=locationFour, locationFive=locationFive, locationSix=locationSix, noneSelected=noneSelected)

@app.route('/thankyou', methods = ['GET', 'POST'])
def thankyou ():
    return render_template ('thankyou.html')

@app.route('/aboutus', methods = ['GET', 'POST'])
def aboutus ():
    return render_template ('aboutus.html')

@app.route('/editprofile', methods = ['GET', 'POST'])
def editprofile():
    email = session.get('email', None)
    profilePic, phoneNumber, aboutMe = False, False, False

    profiles = Profile.query.filter(Profile.email == email).all()
    myProfile = profiles[0]

    dbProfilePic = myProfile.profilePic
    dbPhoneNumber = myProfile.phoneNumber
    dbAboutMe = myProfile.aboutMe

    if request.method == 'POST':
        profilePic = request.form['profilePic']
        phoneNumber = request.form['phoneNumber']
        aboutMe = request.form['aboutMe']

        searchProfiles = Profile.query.filter(Profile.email == email).all()
        getProfile = searchProfiles[0]
        getProfile.profilePic = profilePic
        getProfile.phoneNumber = phoneNumber
        getProfile.aboutMe = aboutMe
        db.session.add(getProfile)
        db.session.commit()

        return redirect(url_for('user', username=email))

    return render_template ('editprofile.html', email=email, dbProfilePic=dbProfilePic, dbPhoneNumber=dbPhoneNumber, dbAboutMe=dbAboutMe)

@app.route('/user/<username>')
def user(username):
    userEmail = username;
    email = session.get('email', None)
    sameUser = False
    searchProfiles = Profile.query.filter(Profile.email == userEmail).all()
    getProfile = searchProfiles[0]

    if userEmail == email:
        sameUser = True;

    searchUsers = User.query.filter(User.email == userEmail).all()
    getUser = searchUsers[0]
    firstName = getUser.firstName
    lastName = getUser.lastName
    fullname = firstName + " " + lastName

    return render_template('user.html', email=email, fullname=fullname, userEmail=userEmail, sameUser=sameUser, getProfile=getProfile)

if __name__ == '__main__':
    app.run(debug=True)

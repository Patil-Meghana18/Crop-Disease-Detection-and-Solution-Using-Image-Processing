from flask import Flask, request, render_template, send_from_directory,flash
from pylab import *
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import cv2
from prediction import livestreaming
import mysql.connector

app=Flask(__name__)
app.secret_key="CBJcb786874wrf78chdchsdcv"




def getdb():
    db=mysql.connector.connect(host="localhost",user="root",password="",port='3306',database='hate_speech')
    cur=db.cursor()
    return db,cur

app=Flask(__name__)
app.secret_key='random string'

classes=['Apple','Apple Black rot','Apple Cedar apple rust','Apple healthy','Blueberry healthy','Corn','Corn Gray leafspot',
'Corn healthy','Grape','Grape healthy','Grape Leaf blight','Orange Haunglongbing','Peach','Tomato']


# Load the pre-trained model
model = load_model(r'alg\cnn.h5')

# Set up video capture device
cap = cv2.VideoCapture(0)



@app.route('/')
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/register',methods=["POST","GET"])
def register():
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']        
        address = request.form['address']        
        contact = request.form['contact']
        db,cur = getdb()
        sql="select * from user where useremail='%s' and userpassword='%s'"%(useremail,userpassword)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        print(data)
        if data==[]:   
            db,cur = getdb()         
            sql = "insert into user(firstname,lastname,useremail,userpassword,address,contact)values(%s,%s,%s,%s,%s,%s)"
            val=(firstname,lastname,useremail,userpassword,address,contact)
            cur.execute(sql,val)
            db.commit()
            flash("Registered successfully","success")
            return render_template("login.html")
        else:
            flash("Details are invalid","warning")
            return render_template("register.html")
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['passw']
        
        user = Register.query.filter_by(email=email, password=password).first()
        
        if user:
            session['user_id'] = user.id
            return redirect(url_for('userhome'))
        else:
            flash("Login failed", "warning")
            return render_template("login.html", msg="Login failed")
    
    return render_template("login.html")

@app.route('/userhome')
def userhome():
    return render_template('userhome.html')



@app.route("/upload")
def upload():
    return render_template("upload.html")
@app.route('/upload1/<filename>')
def send_image(filename):
    print('kjsifhuissywudhj')
    return send_from_directory("images", filename)

@app.route("/upload1", methods=["POST","GET"])
def upload1():
    print('a')
    if request.method=='POST':
        m = int(request.form['alg'])
        myfile = request.files['file']
        print("sdgfsdgfdf")
        fn = myfile.filename
        mypath = os.path.join('images/', fn)
        myfile.save(mypath)

        print("{} is the file name", fn)
        print("Accept incoming file:", fn)
        print("Save it to:", mypath)
        # import tensorflow as tf

        new_model = load_model(r'alg\cnn.h5')
        test_image = image.load_img(mypath, target_size=(256, 256))
        test_image = image.img_to_array(test_image)
        test_image = test_image / 255

        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)

        prediction = classes[np.argmax(result)]
        print(prediction)

        if prediction == 'Apple':
            mssg = "secondary crops:Clover,Fescue Grass."
            pesticides = ""

        elif prediction =='Apple Black rot':
            mssg = "secondary crops:Clover,Buckwheat "
            pesticides = "crop pesticides:Copper-Based Fungicides,Mancozeb"

        elif prediction == 'Apple Cedar apple rust':
            mssg ="secondary crops:Corn ,Sunflowers "
            pesticides = "crop pesticides,Mancozeb,Myclobutanil"

        elif prediction =='Apple healthy':
            mssg = "secondary crops:Clover,Comfrey "
            pesticides =""

        elif prediction == 'Blueberry healthy':
            mssg ="secondary crops:Buckwheat ,Clover"
            pesticides =""

        elif prediction =='Corn':
            mssg = "secondary crops:Soybeans,Winter Cover Crops"
            pesticides = "crop pesticides:Atrazine,Bacillus thuringiensis (Bt) Corn"

        elif prediction == 'Corn Gray leaf':
            mssg ="secondary crops:Soybeans,Alfalfa"
            pesticides = "crop pesticides:Azoxystrobin,Mancozeb"

        elif prediction =='Corn healthy':
            mssg ="secondary crops:Soybeans,Cover Crops"
            pesticides = ""

        elif prediction =='Grape':
            mssg ="secondary crops:Cover Crops,Herbs"
            pesticides = "crop pesticides:Neem Oil ,Sulfur-based Fungicides"

        elif prediction =='Grape healthy':
            mssg ="secondary crops:Soybeans,Cover Crops ."
            pesticides = ""

        elif prediction =='Grape Leaf blight':
            mssg ="secondary crops:Clover,Mustard"
            pesticides = "crop pesticides:Copper-based Fungicides,Triazole Fungicides."

        elif prediction =='Orange Haunglongbing':
            mssg ="secondary crops:Guava,Avocado."
            pesticides = "crop pesticides:Neonicotinoids,Copper-based Fungicides."

        elif prediction =='Peach':
            mssg ="secondary crops:Clover,Marigold"
            pesticides = "crop pesticides:Neem Oil,Captan."

        elif prediction =='Tomato':
            mssg ="secondary crops:Basil,Marigold"
            pesticides = "crop pesticides:Neem Oil,Captan"
    
    
    
    db,cur = getdb()
    sql = "insert into secondary(prediction,secondarycrop,pesticides) values (%s,%s,%s)"
    values = (prediction, mssg, pesticides)
    # Execute the query
    cur.execute(sql, values)
    # Commit the changes and close the connection
    db.commit()
    db.close()
    return render_template("template.html", image_name=fn, text=prediction ,pics=mssg,pesticides=pesticides)




@app.route('/prediction')
def prediction():
    livestreaming()  # Run the livestreaming function for live prediction
    print("Running")
    return render_template('index.html')


if __name__=='__main__':
    app.run(debug=True)
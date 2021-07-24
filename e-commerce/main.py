from flask import Flask,render_template, request,redirect, session,send_from_directory
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from mysql.connector import connect
from flask_mail import Mail, Message
import random
from random import randint
import string
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif'}
otp=0

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:/Users/HP/PycharmProjects/e-commerce/static/uploadedimages/'
app.config['MAX_CONTENT_PATH']= 3145728

app.config.update(
 MAIL_SERVER='smtp.gmail.com',
 MAIL_PORT=465,
 MAIL_USE_SSL=True,
 MAIL_USERNAME='maheshwariashutosh76@gmail.com',
 MAIL_PASSWORD='mukeshgupta@123'
)

app.secret_key="ashashuu123"

mail=Mail(app)

@app.route("/")
def home1():
    return redirect('/index.html')

def getloggingdetail():
    connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
    cur = connection.cursor()
    if "User_Id" not in session:
        loggedIn= False
        First_Name=''
        noOfItems=0
    else:
        loggedIn = True
        query1="select User_Id,First_Name from user_detail where User_Id='{}'".format(session['User_Id'])
        cur.execute(query1)
        User_Id,First_Name=cur.fetchone()
        query2 = "select count(product_id) from cart where User_id='{}'".format(User_Id)
        cur.execute(query2)
        noOfItems=cur.fetchone()[0]
    return (loggedIn,First_Name,noOfItems)






@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/Catagori.html")
def category():

        loggedIn, First_Name, noOfItems = getloggingdetail()
        print(loggedIn)
        print(First_Name)
        print(noOfItems)
        return render_template('Catagori.html',loggedIn=loggedIn,First_Name=First_Name, noOfItems=noOfItems)

@app.route("/index.html")
def index():
        loggedIn, First_Name, noOfItems = getloggingdetail()
        connection = connect(host="localhost", port='3307', database="ashu", user="root", password="ashu@123")
        cur = connection.cursor()
        query = "select * from product_detils"
        cur.execute(query)
        xyz = cur.fetchall()
        print(xyz)
        return render_template('index.html', xyz=xyz,loggedIn=loggedIn,First_Name=First_Name, noOfItems=noOfItems)

@app.route("/admin.html")
def admin():
    connection = connect(host="localhost", port='3307', database="ashu", user="root", password="ashu@123")
    cur = connection.cursor()
    query = "select * from product_detils"
    cur.execute(query)
    xyz = cur.fetchall()
    print(xyz)
    return render_template('admin.html', xyz=xyz)



@app.route("/product_list.html")
def productlist():
    return render_template('product_list.html')

@app.route("/single-product.html")
def single():
    return render_template('single-product.html')

@app.route("/blog.html")
def blog():
    return render_template('blog.html')

@app.route("/single-blog.html")
def sblog():
    return render_template('single-blog.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/profile.html")
def profile():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()
        query1 = "select * from user_detail where User_Id={}".format(Id)
        cur.execute(query1)
        xyz= cur.fetchone()
        print(xyz)
        return render_template('profile1.html',xyz=xyz)
    return render_template("login.html")

@app.route("/edit",methods=['POST'])
def edit():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        id = request.form.get('id')
        email = request.form.get('email')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        zipcode = request.form.get('zipcode')
        city = request.form.get('city')
        phone_no = request.form.get('phone')
        return render_template("edit.html", id=id,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,phone=phone_no)
    return render_template("login.html")


@app.route("/update",methods=['POST'])
def update():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        id = request.form.get('id')
        email = request.form.get('email')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        zipcode = request.form.get('zipcode')
        city = request.form.get('city')
        phone_no=request.form.get('phone')
        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()
        query1 = "update user_detail set EMail ='{}', Address1 ='{}', Address2 ='{}', Zipcode ='{}', City ='{}',Phone_No='{}' where User_Id={}".format(email,address1,address2,zipcode,city,phone_no,id)
        cur.execute(query1)
        connection.commit()
        return redirect('/profile.html')


    return render_template("login.html")





@app.route("/elements.html")
def elements():
    loggedIn, First_Name, noOfItems = getloggingdetail()
    print(loggedIn)
    print(First_Name)
    print(noOfItems)
    return render_template('elements.html',loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)

@app.route("/about.html")
def about():
    return render_template('about.html')



@app.route("/checkout.html")
def checkout1():
    if 'User_Id' in session:
        loggedIn, First_Name, noOfItems = getloggingdetail()
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()

        query = "select product_detils.product_id,product_detils.name,product_detils.prize,product_detils.image,cart.quantity from product_detils,cart where product_detils.product_id=cart.product_id and cart.User_Id={}".format(Id)
        cur.execute(query)
        data = cur.fetchall()
        subtotal = 0
        for row in data:
            subtotal += int(row[2]) * row[4]
        totalprice = subtotal + 50
        return render_template('checkout.html',data=data,totalprice=totalprice,subtotal=subtotal,loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)
    return render_template("login.html")

@app.route("/register3")
def reg():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        First_Name = request.args.get('fname')
        Last_Name = request.args.get('lname')
        Address1 = request.args.get('add1')
        Address2 = request.args.get('add2')
        Zipcode = request.args.get('zip')
        City = request.args.get('city')
        State = request.args.get('state')
        Country = request.args.get('country')
        EMail = request.args.get('email')
        Company = request.args.get('cname')
        Phone_No = request.args.get('number')
       # bdate=date.today()


        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()
        query1 = "select * from user_detail where User_Id={}".format(Id)
        cur.execute(query1)
        xyz = cur.fetchone()
        print(xyz)
        if xyz == None:
            return render_template("signup.html")
        else:
            cur = connection.cursor()
            query2 = "insert into bill(fname,lname,cname,phone_no,email,adreess1,adreess2,city,state,country,zipcode,User_Id) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},{})".format(First_Name, Last_Name, Company, Phone_No, EMail, Address1, Address2, City, State, Country, Zipcode, Id)
            cur.execute(query2)
            abc1 = cur.fetchone()
            connection.commit()
            #print(abc1)
            return redirect("/confirmation.html")
    return render_template("login.html")

@app.route("/contact.html")
def contact():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        return render_template('profile.html')
    return render_template("login.html")


@app.route("/register1",methods=['POST'])
def reg1():

        textarea = request.form.get("message")
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()
        query1 = "select * from contact where Email='{}'".format(email)
        cur.execute(query1)
        xyz = cur.fetchone()
        print(xyz)

        cur = connection.cursor()
        query1 = "insert into contact (Message,Name,Email,Subject) values('{}','{}','{}','{}')".format(textarea, name,email, subject)
        cur.execute(query1)
        connection.commit()
        return redirect("/home1")







@app.route("/forget")
def forget():
    email=request.form.get("email")
    return render_template('forget.html',email=email)

@app.route("/forgetPassword",methods=["POST"])
def forgetPassword():
    global otp
    email=request.form.get("email")
    connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
    cur = connection.cursor()
    query1 = "select * from user_detail where EMail='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if(xyz==None):
        return render_template('forget.html',error="email no exist")
    else:
        otp = randint(1111, 9999)

        return redirect('/mailbhejo')


@app.route("/checkotp",methods=['POST'])
def checkotp():
    email=request.form.get("email")
    otp=request.form.get("OTP")
    connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
    cur = connection.cursor()
    query1 = "select * from user_detail where EMail='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if xyz == None:
        return render_template("forget.html",error="NOT MATCHED!!")
    else:
        return render_template("ResetPassword.html",email=email,otp=otp)

    #return render_template('forget.html',email=email)
    #return render_template('ResetPassword.html')


@app.route('/mailbhejo')
def mailbhejo():
    new = str(otp)
    msg = Message(subject='mail sender', sender='maheshwariashutosh76@gmail.com', recipients=['maheshwariashutosh76@gmail.com'], body=new)
    msg.cc = ['robins20.k@gmail.com']
    email="maheshwariashutosh76@gmail.com"
    mail.send(msg)
    return render_template('OTP.html')

@app.route("/reset",methods=['POST'])
def reset():
    email = request.form.get("email")
    password = request.form.get("pwd")
    connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
    cur = connection.cursor()
    query1 = "update user_detail set Password='{}' where EMail='{}'".format(password, email)
    cur.execute(query1)
    connection.commit()
        # return render_template('ResetPassword.html',otp=OTP,email=email)
    return redirect('/mailbhejo1')

@app.route('/mailbhejo1')
def mailbhejo1():
    msg=Message(subject='mail sender',sender='maheshwariashutosh76@gmail.com', recipients=['maheshwariashutosh76@gmail.com'],body="PASSWORD UPDATES SUCESSFULLY")
    mail.send(msg)
    return render_template("login.html")

@app.route("/register",methods=['POST'])
def register():
    First_Name = request.form.get('firstName')
    Last_Name=request.form.get('lastName')
    Address1=request.form.get('address1')
    Address2=request.form.get('address2')
    Zipcode = request.form.get('zipcode')
    City = request.form.get('city')
    State = request.form.get('state')
    Country = request.form.get('country')
    EMail = request.form.get('email')
    Password = request.form.get('pwd')
    Phone_No = request.form.get('phone')
    connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
    cur = connection.cursor()
    query1 = "select * from user_detail where EMail='{}'".format(EMail)
    cur.execute(query1)
    xyz = cur.fetchone()
    if xyz == None:
        query = "insert into user_detail(First_Name,Last_Name,EMail,Address1,Address2,zipcode,City,State,Country,Password,Phone_No) values('{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}')".format(First_Name,Last_Name,EMail,Address1,Address2,Zipcode,City,State,Country,Password,Phone_No)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        return redirect("/login.html")
    else:
        return 'already regestired'


@app.route('/checklogin',methods=["POST"])
def checklogin():
    EMail=request.form.get('email')
    Password=request.form.get('pwd')
    connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
    cur = connection.cursor()
    query1 = "select * from user_detail where EMail='{}'".format(EMail)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if xyz == None:
        return render_template('login.html',xyz="you are not regestired")

    else:
        if Password==xyz[10]:
            session['EMail']= EMail
            session['User_Id'] = xyz[0]
            query2 = "select * from admin where EMail='{}'".format(EMail)
            cur.execute(query2)
            xyz1 = cur.fetchone()
            if xyz1 == None:
                return redirect('/home1')
            else:
                return redirect("/admin.html")
        else:
            return render_template('login.html', xyz="your password is not correct")



@app.route('/home')
def home():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(id)
        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()
        query1 = "select * from user_detail where User_Id={}".format(id)
        cur.execute(query1)
        data = cur.fetchall()
        print(data)
        return render_template("index.html")
    return render_template("login.html")



@app.route('/logout')
def logout():
    session.pop('User_Id',None)
    return render_template("login.html")


@app.route('/home1')
def ho():
    loggedIn, First_Name, noOfItems = getloggingdetail()
    connection = connect(host="localhost", port='3307', database="ashu", user="root", password="ashu@123")
    cur = connection.cursor()
    query = "select * from product_detils"
    cur.execute(query)
    xyz = cur.fetchall()
    print(xyz)
    return render_template("index1.html",xyz=xyz,loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)


@app.route("/add")
def add():
    connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
    cur = connection.cursor()
    query1 = "select category_id,name from categories"
    cur.execute(query1)
    data = cur.fetchall()
    return render_template("add.html",data=data)

@app.route("/addItem",methods=['POST'])
def additem():
    name = request.form.get('name')
    price = request.form.get('price')
    description=request.form.get('description')
    stock = request.form.get('stock')
    categoryId = request.form.get('category')
    if request.method == 'POST':
        if 'img' not in request.files:
            print("file not uploaded")
        f = request.files['img']
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))
        image= f.filename
        print("file uploaded")

    connection = connect(host="localhost", port='3307', database="ashu", user="root", password="ashu@123")
    cur = connection.cursor()

    query = "insert into product_detils(name,prize,description,stock,category_id,image) values('{}','{}','{}',{},{},'{}')".format(name,price, description,stock,categoryId,image)

    cur.execute(query)
    connection.commit()
    return render_template('admin.html')

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("static/uploadedimages/", filename)



@app.route("/men.html")
def men():
    loggedIn, First_Name, noOfItems = getloggingdetail()
    connection = connect(host="localhost", port='3307', database="ashu", user="root", password="ashu@123")
    cur = connection.cursor()
    query="select * from product_detils where category_id='1'"
    cur.execute(query)
    xyz= cur.fetchall()
    print(xyz)
    return render_template('men.html',xyz=xyz,loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)

@app.route("/women.html")
def women():
    loggedIn, First_Name, noOfItems = getloggingdetail()
    connection = connect(host="localhost", port='3307', database="ashu", user="root", password="ashu@123")
    cur = connection.cursor()
    query="select * from product_detils where category_id='2'"
    cur.execute(query)
    xyz= cur.fetchall()
    print(xyz)
    return render_template('women.html',xyz=xyz,loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)

@app.route("/kids.html")
def kids():
    loggedIn, First_Name, noOfItems = getloggingdetail()
    connection = connect(host="localhost", port='3307', database="ashu", user="root", password="ashu@123")
    cur = connection.cursor()
    query="select * from product_detils where category_id='3'"
    cur.execute(query)
    xyz= cur.fetchall()
    print(xyz)
    return render_template('kids.html',xyz=xyz,loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)



@app.route("/addcart",methods=['POST'])
def acart():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        product_id=request.form.get("product_id")
        quantity= request.form.get("quantity")
        print(quantity)
        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()
        query1 = "select * from user_detail where User_Id={}".format(Id)
        cur.execute(query1)
        xyz=cur.fetchone()[0]
        print(xyz)
        query2="insert into cart(User_Id,product_id,quantity) values({},{},{})".format(xyz,product_id,quantity)
        cur.execute(query2)
        xyz1=cur.fetchone()
        connection.commit()
        #print(xyz)
        query3 = "insert into cart1(User_Id,product_id,quantity) values({},{},{})".format(xyz, product_id, quantity)
        cur.execute(query3)
        connection.commit()

        return redirect("/cart.html")
    return render_template("login.html")


@app.route("/productdes")
def prod():
    loggedIn,First_Name,noOfItems=getloggingdetail()

    product_id=request.args.get('product_id')
    connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
    cur = connection.cursor()
    query1 = "select product_id,name,prize,description,stock,image from product_detils where product_id='{}'".format(product_id)
    cur.execute(query1)
    data=cur.fetchall()
    print(data)
   # print(data)
    return render_template("product des.html",data=data,loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)

@app.route("/cart.html")
def cart():
    loggedIn, First_Name, noOfItems = getloggingdetail()
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)

        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()
        query="select User_Id from user_detail where User_Id='{}'".format(Id)
        cur.execute(query)
        xyz=cur.fetchone()[0]
        print(xyz)
        query1 = "select product_detils.product_id,product_detils.name,product_detils.prize,product_detils.image,cart.quantity from product_detils,cart where product_detils.product_id=cart.product_id and cart.User_Id={}".format(xyz)
        cur.execute(query1)
        data = cur.fetchall()
        totalprice=0
        for row in data:
            totalprice+=int(row[2])*row[4]
    return render_template('cart.html',data=data,totalprice=totalprice,loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)

@app.route("/remove",methods=['POST'])
def remove():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        product_id = request.form.get('product_id')
        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()
        query="delete from cart where User_Id={} and product_id={}".format(Id,product_id)
        cur.execute(query)
        connection.commit()
        return  redirect("/cart.html")

@app.route("/buy")
def buy():
    return redirect("/checkout.html")

@app.route("/confirmation.html")
def confirmation():
    loggedIn, First_Name, noOfItems = getloggingdetail()
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()

        query1 = "select product_detils.product_id,product_detils.name,product_detils.prize,product_detils.image,cart.quantity from product_detils,cart where product_detils.product_id=cart.product_id and cart.User_Id={}".format(Id)
        cur.execute(query1)
        data = cur.fetchall()
        print(data)
        subtotal = 0
        for row in data:
            subtotal += int(row[2]) * row[4]
        totalprice = subtotal + 50

        query = "select * from bill where User_Id={}  ORDER BY  bill.order_id DESC".format(Id)
        cur.execute(query)
        abc = cur.fetchone()
        print(abc)

        return render_template('confirmation.html', abc=abc,data=data,subtotal=subtotal,totalprice=totalprice,loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)


    return render_template("login.html")

@app.route("/coniform")
def con():
    if 'User_Id' in session:
        loggedIn, First_Name, noOfItems = getloggingdetail()
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()
        query = "delete from cart where User_Id={}".format(Id)
        cur.execute(query)
        connection.commit()
        return render_template("coniform.html",loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)

    return render_template("login.html")

@app.route("/order")
def order():
    if 'User_Id' in session:
        EMail = session['EMail']
        Id = session['User_Id']
        print(Id)
        #bdate = datetime.now()
        connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
        cur = connection.cursor()
        query1 = "select product_detils.product_id,product_detils.name,product_detils.prize,product_detils.image,cart1.quantity from product_detils,cart1 where product_detils.product_id=cart1.product_id and cart1.User_Id={}".format(Id)
        cur.execute(query1)
        xyz1 = cur.fetchall()
        print(xyz1)
        query = "Select bill.order_id,bill.booking_data,bill.adreess1,bill.email from bill where User_Id={}".format(Id)
        cur.execute(query)
        xyz=cur.fetchall()
        print(xyz)

        return render_template("order.html",xyz=xyz,xyz1=xyz1)
    return render_template("login.html")

@app.route("/search")
def search():
    name=request.args.get("Search")
    connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
    cur = connection.cursor()
    query="select name from categories where name='{}'".format(name)
    cur.execute(query)
    xyz= cur.fetchone()
    print(str(xyz))
    print(xyz)
    if xyz == ("child wear",):
        return redirect("/kids.html")
    elif xyz == ("mens wear",):
        return redirect("/men.html")
    else:
        return redirect("/women.html")

@app.route("/query")
def query():
    connection = connect(host='localhost', port='3307', database='ashu', user='root', password='ashu@123')
    cur = connection.cursor()
    query = "select Message,Name,Email,Subject from contact"
    cur.execute(query)
    xyz = cur.fetchall()
    return render_template("query.html",xyz=xyz)

@app.route("/sort")
def sort():
    loggedIn, First_Name, noOfItems = getloggingdetail()
    connection = connect(host="localhost", port='3307', database="ashu", user="root", password="ashu@123")
    cur = connection.cursor()
    query="select * from product_detils where category_id='1'"
    cur.execute(query)
    xyz= cur.fetchall()
    print(xyz)
    return render_template('men.html',xyz=xyz,loggedIn=loggedIn,First_Name=First_Name,noOfItems=noOfItems)























if __name__ =='__main__':
    app.run()
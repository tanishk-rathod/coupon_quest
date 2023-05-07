from flask import Flask,render_template,request,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from datetime import datetime
import os,json,math

with open("config.json") as c:
    params=json.load(c)["Params"]

db=SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1/DisCode"
app.secret_key = 'secret key'

db=SQLAlchemy(app)

from models import User, quizQues, quizDes, quiz_result, Contact, ClientUser, Coupon
from forms import RegistrationForm, LoginForm, ContactForm,ClientLoginForm ,AdminLoginForm, ClientRegistrationForm,CouponForm,QuizForm,QuesForm

@app.route("/")
def home():
    quizes = quizDes.query.filter_by().all()
    if 'user' in session:
        return render_template('index.html', username=session["user"],quizes=quizes,params=params,page=1)
    return render_template("index.html",quizes=quizes,params=params,page=1)

@app.route("/contact", methods=['GET','POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        entry = Contact(Name=form.name.data,Email=form.email.data,Subject=form.subject.data,Message=form.message.data)
        db.session.add(entry)
        db.session.commit()
        return redirect('/') 
    return render_template('contact.html',form=form ,type='about',params=params,page=5)


@app.route("/about")
def about():
    return render_template('about.html',type='about',params=params,page=2)

@app.route("/testimonials")
def tesitmonials():
    return render_template('testimonials.html',params=params,page=3)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if(request.method=='POST'):
        user = User.query.filter_by(Email=form.email.data).first()
        if(user==None):
            return redirect("/login")
        
        
        if (user.Password==form.password.data):
            session['user']=user.Name
            return redirect("/")

    return render_template("login.html",form=form,params=params, page=6)

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        entry = User(Name=form.name.data,Email=form.email.data,Phone_num=form.phone.data,Password=form.password.data)
        db.session.add(entry)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect('/')

    return render_template("register.html", form=form,params=params)
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect("/")

@app.route("/quiz")
def quiz():
    quizes = quizDes.query.filter_by().all()
    return render_template("quiz.html",quizes=quizes,params=params,page=4)


@app.route("/quiz-details/<string:quiz_no>")
def quiz_details(quiz_no):
    quiz = quizDes.query.filter_by(Quiz_no=quiz_no).first()
    status = 0
    if quiz.contest == 'Active' :
        result = quiz_result.query.filter_by(Name=session['user']).all()  
        for resul in result:
            if resul.Quiz_no == quiz.Quiz_no:
                status = 1
    return render_template('quiz-details.html',quiz=quiz,status=status,params=params)


@app.route("/ques/<string:quiz_no>/<string:ques_no>",methods=['GET', 'POST'])
def ques(quiz_no, ques_no, point=0):
    Quess = quizQues.query.filter_by(Quiz_no=quiz_no).all()
    number_of_ques = len(Quess)-1
    Ques = Quess[int(ques_no)]
    if ques_no=='0':
        session['marks'] = 0
        global datetime
        datetime = datetime.now()
    
    if request.method=="POST":
        response = request.form.get("res")
        if response == Ques.Answer:
            session['marks'] += 10
        print(session['marks'])
        if int(ques_no) < number_of_ques:
            stri = f'/ques/{quiz_no}/{str(int(ques_no)+1)}'
            return redirect(stri)
        stri = f'/recent_score/{quiz_no}'
        return redirect(stri)
    return render_template("ques.html",Ques=Ques,ques_no=ques_no,params=params)

@app.route("/recent_score/<string:quiz_no>", methods=['GET'])
def recent_score(quiz_no):

    user = User.query.filter_by(Name=session['user']).first()
    if quiz_result.query.filter_by(Name=session['user'],Quiz_no=quiz_no).first():
        user_result=quiz_result.query.filter_by(Name=session['user'],Quiz_no=quiz_no).first()
        user_result.Point = session['marks']
        user_result.start_Date_time = datetime
        user_result.end_Date_time = datetime.now()
        db.session.merge(user_result)
        db.session.commit()
    else:
        entry = quiz_result(Name=session['user'],Quiz_no=int(quiz_no),Point=session['marks'],start_Date_time=datetime,end_Date_time=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template("recent_score.html", points=session['marks'], quiz_no = quiz_no,params=params)

@app.route("/result", methods=['GET'])
def result():
    result = quiz_result.query.filter_by(Name=session['user']).all()
    return render_template('result.html',result=result,params=params,page=7)

@app.route("/client_login", methods=['GET', 'POST'])
def client_login():
    form = ClientLoginForm()
    if(request.method=='POST'):
        clientuser = ClientUser.query.filter_by(Email=form.email.data).first()
        if(clientuser==None):
            return redirect("/client_login")
                
        if (clientuser.Password==form.password.data):
            session['client_user']=clientuser.Client_Name
            return redirect("/client_portal")

    return render_template("client_login.html",form=form,params=params)

@app.route("/client_portal", methods=['GET', 'POST'])
def client_portal():
    form = CouponForm()
    if(request.method=='POST'):
        coupon = Coupon.query.filter_by(Coupon_code=form.coupon_code.data).first()
        if(coupon==None):
            return render_template("client_portal.html",params=params, form=form,username=session['client_user'])
        else:
            return render_template("client_portal.html",params=params, form=form,username=session['client_user'],coupon=coupon)
    return render_template("client_portal.html",params=params, form=form,username=session['client_user'])

    # return render_template("client_login.html",form=form,params=params)

@app.route("/redeem/<string:coupon_code>", methods=['GET', 'POST'])
def redeem(coupon_code):
    coupon = Coupon.query.filter_by(Coupon_code=coupon_code).first()
    coupon.Status = 'Used'
    db.session.commit()
    return redirect("/client_portal")

@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if(request.method=='POST'):
        if (form.email.data==params["admin_username"] and form.password.data==params["admin_password"]):
            return render_template("admin_portal.html",params=params)

    return render_template("admin_login.html",form=form,params=params)



@app.route("/add_client", methods=['GET','POST'])
def add_client():
    form = ClientRegistrationForm()
    if form.validate_on_submit():
        entry = ClientUser(Client_Name=form.name.data,Email=form.email.data,Phone_num=form.phone.data,Password=form.password.data)
        db.session.add(entry)
        db.session.commit()
        flash(f'Account created for client {form.name.data}!', 'success')
        return redirect('/')

    return render_template("add_client.html", form=form,params=params)

@app.route("/quiz_portal", methods=['GET', 'POST'])
def quiz_portal():
    quizes = quizDes.query.filter_by().all()
    return render_template("quiz_portal.html",params=params,quizes=quizes)

@app.route("/ques_portal", methods=['GET', 'POST'])
def ques_portal():
    quess = quizQues.query.filter_by().all()
    return render_template("ques_portal.html",params=params,quess=quess)


@app.route("/edit_quiz/<string:sno>", methods=['GET', 'POST'])
def edit_quiz(sno):
    form = QuizForm()
    if(request.method=="POST"):
        if(sno=="0"):
            entry = quizDes(Quiz_no=form.quiz_no.data,Quiz_sub=form.quiz_sub.data,Quiz_cate=form.quiz_cate.data,Quiz_des=form.quiz_des.data,img_file1=form.img_file1.data,img_file2=form.img_file2.data,img_file3=form.img_file3.data,Date_time=datetime.now().date())
            db.session.add(entry)
            db.session.commit()
            return redirect('/quiz_portal')

        else:
            quiz = quizDes.query.filter_by(S_no=sno).first()

            quiz.Quiz_no = form.quiz_no.data
            quiz.Quiz_sub = form.quiz_sub.data
            quiz.Quiz_cate = form.quiz_cate.data
            quiz.Quiz_des = form.quiz_des.data
            quiz.img_file1 = form.img_file1.data
            quiz.img_file2 = form.img_file2.data
            quiz.img_file3 = form.img_file3.data
            db.session.commit()
            return redirect('/quiz_portal')
    quiz = quizDes.query.filter_by(S_no=sno).first()
    return render_template("edit_quiz.html",params=params,sno=sno,quiz=quiz,form=form)

@app.route("/edit_ques/<string:sno>", methods=['GET', 'POST'])
def edit_ques(sno):
    form = QuesForm()
    if(request.method=="POST"):
        if(sno=="0"):
            entry = quizQues(Quiz_no=form.quiz_no.data,Ques=form.ques.data,A=form.A.data,B=form.B.data,C=form.C.data,D=form.D.data,Answer=form.answer.data,Date_time=datetime.now())
            db.session.add(entry)
            db.session.commit()
            return redirect('/ques_portal')

        else:
            ques = quizDes.query.filter_by(S_no=sno).first()

            ques.Quiz_no = form.quiz_no.data
            ques.Ques = form.ques.data
            ques.A = form.A.data
            ques.B = form.B.data
            ques.C = form.C.data
            ques.D = form.D.data
            ques.Answer = form.answer.data
            db.session.commit()
            return redirect('/ques_portal')
    ques = quizQues.query.filter_by(S_no=sno).first()
    return render_template("edit_ques.html",params=params,sno=sno,ques=ques,form=form)


@app.route('/delete/<string:type>/<string:sno>',methods=['POST','GET'])
def delete(sno,type):
    if(type=='quiz'):
        quiz = quizDes.query.filter_by(S_no=sno).first()
        db.session.delete(quiz)
        db.session.commit()
        return redirect("/quiz_portal")
    else:
        ques = quizQues.query.filter_by(S_no=sno).first()
        db.session.delete(ques)
        db.session.commit()
        return redirect("/quiz_portal")





app.run(debug=True)


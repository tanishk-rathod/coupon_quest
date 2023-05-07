from __main__ import db

class User(db.Model):
    S_no = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), primary_key=False, nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Phone_num = db.Column(db.Integer, primary_key=False, nullable=False)
    Password = db.Column(db.String(50), nullable=False)

class ClientUser(db.Model):
    S_no = db.Column(db.Integer, primary_key=True)
    Client_Name = db.Column(db.String(80), primary_key=False, nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Phone_num = db.Column(db.Integer, primary_key=False, nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    
class Coupon(db.Model):
    S_no = db.Column(db.Integer, primary_key=True)
    Coupon_code = db.Column(db.String(80), primary_key=False, nullable=False)
    Dis_percentage = db.Column(db.Integer, primary_key=False, nullable=False)
    Date_rewarded = db.Column(db.String(12),nullable=False,primary_key=False)
    Expiry_date = db.Column(db.String(12),nullable=False,primary_key=False)
    Status = db.Column(db.String(12),nullable=False,primary_key=False)

class quizQues(db.Model):
    S_no = db.Column(db.Integer, primary_key=True)
    Quiz_no = db.Column(db.Integer, primary_key=False)
    Ques = db.Column(db.String(200), primary_key=False, nullable=False)
    A = db.Column(db.String(50), nullable=False)
    B = db.Column(db.String(50), nullable=False)
    C = db.Column(db.String(50), nullable=False)
    D = db.Column(db.String(50), nullable=False)
    Answer = db.Column(db.String(50), nullable=False)
    Date_time = db.Column(db.String(12),nullable=False,primary_key=False)
class quizDes(db.Model):
    S_no = db.Column(db.Integer, primary_key=True)
    Quiz_no = db.Column(db.Integer, primary_key=False)
    Quiz_sub = db.Column(db.String(50), primary_key=False, nullable=False)
    Quiz_cate = db.Column(db.String(20), primary_key=False, nullable=False)
    Quiz_des = db.Column(db.String(200), primary_key=False, nullable=False)
    img_file1 = db.Column(db.String(50), nullable=False)
    img_file2 = db.Column(db.String(50), nullable=False)
    img_file3 = db.Column(db.String(50), nullable=False)
    Date_time = db.Column(db.String(12),nullable=False,primary_key=False)
    contest = db.Column(db.String(12),nullable=False,primary_key=False)
    
class quiz_result(db.Model):
    S_no = db.Column(db.Integer, primary_key=True)
    Quiz_no = db.Column(db.Integer, primary_key=False)
    Name = db.Column(db.String(50), nullable=False)
    Point = db.Column(db.Integer, primary_key=False)
    start_Date_time = db.Column(db.String(12),nullable=False,primary_key=False)
    end_Date_time = db.Column(db.String(12),nullable=False,primary_key=False)

class Contact(db.Model):
    S_no = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Subject = db.Column(db.String(50), nullable=False)
    Message = db.Column(db.String(200), nullable=False)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo




class RegistrationForm(FlaskForm):
    name = StringField(
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(
                        validators=[DataRequired(), Email()])
    phone = StringField(
                        validators=[DataRequired(), Length(10)])
    password = PasswordField( validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField(
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
class ClientRegistrationForm(FlaskForm):
    name = StringField(
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(
                        validators=[DataRequired(), Email()])
    phone = StringField(
                        validators=[DataRequired(), Length(10)])
    password = PasswordField( validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField(
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class CouponForm(FlaskForm):
    coupon_code = StringField(
                           validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField(
                        validators=[DataRequired(), Email()])
    password = PasswordField( validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ClientLoginForm(FlaskForm):
    email = StringField(
                        validators=[DataRequired(), Email()])
    password = PasswordField( validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
class AdminLoginForm(FlaskForm):
    email = StringField(
                        validators=[DataRequired(), Email()])
    password = PasswordField( validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ContactForm(FlaskForm):
    name = StringField(
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(
                        validators=[DataRequired(), Email()])
    subject = StringField(
                           validators=[DataRequired(), Length(min=2, max=50)])
    message = StringField(
                           validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Send Message')


class QuizForm(FlaskForm):
    quiz_no = StringField(validators=[DataRequired()])
    quiz_sub = StringField(validators=[DataRequired()])
    quiz_cate = StringField(validators=[DataRequired()])
    quiz_des = StringField(validators=[DataRequired()])
    img_file1 = StringField(validators=[DataRequired()])
    img_file2 = StringField(validators=[DataRequired()])
    img_file3 = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')

class QuesForm(FlaskForm):
    quiz_no = StringField(validators=[DataRequired()])
    ques = StringField(validators=[DataRequired()])
    A = StringField(validators=[DataRequired()])
    B = StringField(validators=[DataRequired()])
    C = StringField(validators=[DataRequired()])
    D = StringField(validators=[DataRequired()])
    answer = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')






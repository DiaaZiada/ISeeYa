from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, InputRequired

class IwannaForm(FlaskForm):
    type = SelectField(u'Field name', choices=[('New Service', 'New Service'), ('New Feature', 'New Feature'), ('Issue', 'Issue')])
    content = TextAreaField('Discription', validators=[DataRequired()])
    submit = SubmitField('Submit')

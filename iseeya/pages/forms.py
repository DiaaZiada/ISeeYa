from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, InputRequired

class PageForm(FlaskForm):
    page_name = StringField('Page Name', validators=[DataRequired(), Length(min=2, max=20)])
    page_title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit')

class CoverForm(FlaskForm):
    page = SelectField(u'Page name', coerce=str)
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ItemForm(FlaskForm):
    page = SelectField(u'Page name', coerce=str)
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    link = SelectField(u'Page name', coerce=str)
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ContentForm(FlaskForm):
    page = SelectField(u'Page name', coerce=str)
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


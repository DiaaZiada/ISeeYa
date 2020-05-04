from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from iseeya import db
from iseeya.models import Iwanna
from iseeya.iwanna.forms import IwannaForm

iwanna = Blueprint('iwanna', __name__)


@iwanna.route("/iwanna/a_", methods=['GET', 'POST'])
@login_required
def new_item():
    form = IwannaForm()
    if form.validate_on_submit():
        iwanna = Iwanna(type=form.type.data, content=form.content.data, user_id=current_user.id)
        db.session.add(iwanna)
        db.session.commit()
        flash('Your Wish has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_wish.html', title='New Post',
                           form=form, legend='New Post')

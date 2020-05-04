from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from iseeya import db
from iseeya.models import Page, Cover, Item, SubItem, Content
from iseeya.pages.forms import PageForm, ItemForm 
from iseeya.pages.utils import save_picture

pages = Blueprint('pages', __name__)


@pages.route("/<string:page_name>/", methods=['GET', 'POST'])
def page(page_name):
    page = Page.query.filter_by(name=page_name).first_or_404()
    cover = Cover.query.filter_by(page_id=page.id).first()
    items = Item.query.filter_by(page_id=page.id)
    sub_items = SubItem.query.filter_by(page_id=page.id)
    content = Content.query.filter_by(page_id=page.id).first()
    x=1
    def update():
        nonlocal x
        x+=1
        if x %2==0:
            return True
        return False
    return render_template('page.html', title='New Item',
                    page=page, cover=cover, items=items, 
                    sub_items=sub_items, legend='New Item',update=update, content=content)


from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from iseeya import db
from iseeya.models import Page, Cover, Item, SubItem, Content, Iwanna, User
from iseeya.pages.forms import PageForm, ItemForm, CoverForm, ContentForm
from iseeya.pages.utils import save_picture, delete_picture

admin = Blueprint('admin', __name__)

image_size =  (700, 700)
@admin.route("/admin/new_item", methods=['GET', 'POST'])
@login_required
def new_item():
    if not current_user.is_admin:
        abort(403)
    form = ItemForm()
    form.page.choices= [(p.name, p.name) for i, p in enumerate(Page.query.all())]
    form.link.choices= [(p.name, p.name) for i, p in enumerate(Page.query.all())]
    if form.validate_on_submit():
        global image_size
        page = Page.query.filter_by(name=form.page.data).first_or_404()
        picture_file = save_picture(form.picture.data, image_size)
        item = Item(image_file=picture_file, content=form.content.data, link=form.link.data, page_id=page.id)
        db.session.add(item)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('pages.page', page_name='home'))
    return render_template('create_item.html', title='New Item',
                           form=form, legend='New Item')

@admin.route("/admin/update_item/<int:item_id>", methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if not current_user.is_admin:
        abort(403)
    
    item = Item.query.get_or_404(item_id)
    page = Page.query.filter_by(id=item.page_id).first_or_404()
    choices = []
    choices.append((page.name, page.name))
    for p in Page.query.all():
        if p is not page:
            choices.append((p.name, p.name))
    form = ItemForm()
    form.page.choices = choices
    form.link.choices = choices
    if form.validate_on_submit():
        page = Page.query.filter_by(name=form.page.data).first_or_404()
        item.page_id = page.id
        if form.picture.data:
            global image_size
            delete_picture(item.image_file)
            picture_file = save_picture(form.picture.data, image_size)
            item.image_file = picture_file
        item.content = form.content.data
        item.link = form.link.data
        db.session.commit()
        flash('Item has been updated!', 'success')
        return redirect(url_for('pages.page', page_name='home'))
    form.link.data = item.link
    form.content.data = item.content
    return render_template('create_item.html', title='Update Item',
                           form=form, legend='Update Item')


@admin.route("/admin/delete_item/<int:item_id>", methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if not current_user.is_admin:
        abort(403)
    item = Item.query.get_or_404(item_id)
    delete_picture(item.image_file)
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted!', 'success')
    return redirect(url_for('pages.page', page_name='home'))




@admin.route("/admin/new_subitem", methods=['GET', 'POST'])
@login_required
def new_subitem():
    if not current_user.is_admin:
        abort(403)
    form = ItemForm()
    form.page.choices= [(p.name, p.name) for i, p in enumerate(Page.query.all())]
    form.link.choices= [(p.name, p.name) for i, p in enumerate(Page.query.all())]
    if form.validate_on_submit():
        global image_size
        page = Page.query.filter_by(name=form.page.data).first_or_404()
        picture_file = save_picture(form.picture.data, image_size)
        subitem = SubItem(image_file=picture_file, content=form.content.data, link=form.link.data, page_id=page.id)
        db.session.add(subitem)
        db.session.commit()
        flash('SubItem has been created!', 'success')
        return redirect(url_for('pages.page', page_name='home'))
    return render_template('create_item.html', title='New SubItem',
                           form=form, legend='New SubItem')

@admin.route("/admin/update_subitem/<int:subitem_id>", methods=['GET', 'POST'])
@login_required
def update_subitem(subitem_id):
    if not current_user.is_admin:
        abort(403)
    subitem = SubItem.query.get_or_404(subitem_id)
    # if post.author != current_user:
    #     abort(403)
    
    page = Page.query.filter_by(id=subitem.page_id).first_or_404()

    choices = []
    choices.append((page.name, page.name))
    for p in Page.query.all():
        if p is not page:
            choices.append((p.name, p.name))
    form = ItemForm()
    form.page.choices = choices
    form.link.choices= choices
    if form.validate_on_submit():
        page = Page.query.filter_by(name=form.page.data).first_or_404()
        subitem.page_id = page.id
        if form.picture.data:
            delete_picture(subitem.image_file)
            global image_size
            picture_file = save_picture(form.picture.data, image_size)
            subitem.image_file = picture_file
        subitem.content = form.content.data
        subitem.link = form.link.data
        db.session.commit()
        flash('Item has been updated!', 'success')
        return redirect(url_for('pages.page', page_name='home'))
    form.link.data = subitem.link
    form.content.data = subitem.content
    return render_template('create_item.html', title='Update SubItem',
                           form=form, legend='Update SubItem')




@admin.route("/admin/delete_subitem/<int:subitem_id>", methods=['GET', 'POST'])
@login_required
def delete_subitem(subitem_id):
    if not current_user.is_admin:
        abort(403)
    subitem = SubItem.query.get_or_404(subitem_id)
    delete_picture(subitem.image_file)
    db.session.delete(subitem)
    db.session.commit()
    flash('SubItem has been deleted!', 'success')
    return redirect(url_for('pages.page', page_name='home'))



@admin.route("/admin/new_cover", methods=['GET', 'POST'])
@login_required
def new_cover():
    if not current_user.is_admin:
        abort(403)
    form = CoverForm()
    form.page.choices= [(p.name, p.name) for i, p in enumerate(Page.query.all())]
    if form.validate_on_submit():
        page = Page.query.filter_by(name=form.page.data).first_or_404()
        picture_file = save_picture(form.picture.data)
        cover = Cover(image_file=picture_file, content=form.content.data, page_id=page.id)
        db.session.add(cover)
        db.session.commit()
        flash('Cover has been created!', 'success')
        return redirect(url_for('pages.page', page_name='home'))
    return render_template('create_cover.html', title='New Cover',
                           form=form, legend='New Cover')


@admin.route("/admin/update_cover/<int:cover_id>", methods=['GET', 'POST'])
@login_required
def update_cover(cover_id):
    if not current_user.is_admin:
        abort(403)
    cover = Cover.query.get_or_404(cover_id)
    # if post.author != current_user:
    #     abort(403)
    
    page = Page.query.filter_by(id=cover.page_id).first_or_404()
    choices = []
    choices.append((page.name, page.name))
    for p in Page.query.all():
        if p is not page:
            choices.append((p.name, p.name))
    form = CoverForm()
    form.page.choices = choices
    if form.validate_on_submit():
        page = Page.query.filter_by(name=form.page.data).first_or_404()
        cover.page_id = page.id
        if form.picture.data:
            delete_picture(cover.image_file)
            picture_file = save_picture(form.picture.data)
            cover.image_file = picture_file
        cover.content = form.content.data
        db.session.commit()
        flash('Cover has been updated!', 'success')
        return redirect(url_for('pages.page', page_name='home'))
    form.content.data = cover.content
    return render_template('create_cover.html', title='Update Cover',
                           form=form, legend='Update Cover')


@admin.route("/admin/delete_cover/<int:cover_id>", methods=['GET', 'POST'])
@login_required
def delete_cover(cover_id):
    if not current_user.is_admin:
        abort(403)
    cover = Cover.query.get_or_404(cover_id)
    delete_picture(cover.image_file)
    db.session.delete(cover)
    db.session.commit()
    flash('Cover has been deleted!', 'success')
    return redirect(url_for('pages.page', page_name='home'))




@admin.route("/admin/new_content", methods=['GET', 'POST'])
@login_required
def new_content():
    if not current_user.is_admin:
        abort(403)
    if not current_user.is_admin:
        abort(403)
    form = ContentForm()
    form.page.choices= [(p.name, p.name) for i, p in enumerate(Page.query.all())]
    if form.validate_on_submit():
        page = Page.query.filter_by(name=form.page.data).first_or_404()
        content = Content(content=form.content.data, page_id=page.id)
        db.session.add(content)
        db.session.commit()
        flash('Content has been created!', 'success')
        return redirect(url_for('pages.page', page_name='home'))
    return render_template('create_content.html', title='New Content',
                           form=form, legend='New Content')



@admin.route("/admin/update_content/<int:content_id>", methods=['GET', 'POST'])
@login_required
def update_content(content_id):
    if not current_user.is_admin:
        abort(403)
    content = Content.query.get_or_404(content_id)
    # if post.author != current_user:
    #     abort(403)
    
    page = Page.query.filter_by(id=content.page_id).first_or_404()
    choices = []
    choices.append((page.name, page.name))
    for p in Page.query.all():
        if p is not page:
            choices.append((p.name, p.name))
    form = ContentForm()
    form.page.choices = choices
    if form.validate_on_submit():
        page = Page.query.filter_by(name=form.page.data).first_or_404()
        content.page_id = page.id
        content.content = form.content.data
        db.session.commit()
        flash('Content has been updated!', 'success')
        return redirect(url_for('pages.page', page_name='home'))
    form.content.data = content.content
    return render_template('create_content.html', title='Update Content',
                           form=form, legend='Update Content')

@admin.route("/admin/delete_content/<int:content_id>", methods=['GET', 'POST'])
@login_required
def delete_content(content_id):
    if not current_user.is_admin:
        abort(403)
    content = Content.query.get_or_404(content_id)
    # if post.author != current_user:
    #     abort(403)
    db.session.delete(content)
    db.session.commit()
    flash('Content has been deleted!', 'success')
    return redirect(url_for('pages.page', page_name='home'))


@admin.route("/admin/new_page", methods=['GET', 'POST'])
@login_required
def new_page():
    if not current_user.is_admin:
        abort(403)
    form = PageForm()
    if form.validate_on_submit():
        page = Page(name=form.page_name.data, title=form.page_title.data)
        db.session.add(page)
        db.session.commit()
        flash('Page has been created!', 'success')
        return redirect(url_for('pages.page', page_name='home'))
    return render_template('create_page.html', title='New Item',
                           form=form, legend='New Item')





@admin.route("/admin/update_page/<int:page_id>", methods=['GET', 'POST'])
@login_required
def update_page(page_id):
    if not current_user.is_admin:
        abort(403)
    # if post.author != current_user:
    #     abort(403)
    
    form = PageForm()
    if form.validate_on_submit():
        page = Page.query.get_or_404(page_id)
        page.name = form.page_name.data
        page.title = form.page_title.data
        db.session.commit()
        flash('PAge has been updated!', 'success')
        return redirect(url_for('pages.page', page_name='home'))
    return render_template('create_page.html', title='Update Page',
                           form=form, legend='Update page')



@admin.route("/admin/delete_page/<int:page_id>",  methods=['GET', 'POST'])
@login_required
def delete_page(page_id):
    if not current_user.is_admin:
        abort(403)
    page = Page.query.get_or_404(page_id)
    # if post.author != current_user:
    #     abort(403)
    db.session.delete(page)
    db.session.commit()
    flash('Page has been deleted!', 'success')
    return redirect(url_for('pages.page', page_name='home'))


    
@admin.route("/admin/admin",  methods=['GET', 'POST'])
@login_required
def admin_page():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    wishs = Iwanna.query.all()
    def user(user_id):
        user = User.query.filter_by(id=user_id).first_or_404()
        return user.email
    return render_template("admin.html", wishs=wishs[::-1], user=user, n_users = len(users))


    
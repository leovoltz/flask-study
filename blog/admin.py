from datetime import datetime
from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib.pymongo import ModelView
from flask_simplelogin import login_required
from wtforms import form, fields, validators
from blog.database import mongo
from slugify import slugify


AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
ModelView._handle_view = login_required(AdminIndexView._handle_view)


class PostsForm(form.Form):
    title = fields.StringField("Title", [validators.data_required()])
    slug = fields.HiddenField("Slug")
    content = fields.TextAreaField("Content")
    published = fields.BooleanField("Published", default=True)


class AdminPosts(ModelView):
    column_list = ("title", "slug", "content", "published")
    form = PostsForm

    def on_model_change(self, form, post, is_created):
        post["slug"] = slugify(post["title"])
        if is_created:
            post["date"] = datetime.now()


def configure(app):
    """Starts a Flask-Admin instance"""
    app.admin = Admin(
        app,
        name=app.config.get("TITLE"),
        template_mode=app.config.get(
            "FLASK_ADMIN_TEMPLATE_MODE", "bootstrap3"
        ),
    )
    app.admin.add_view(AdminPosts(mongo.db.posts, "Post"))

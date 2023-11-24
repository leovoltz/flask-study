from flask_simplelogin import login_required
from slugify import slugify
from blog.auth import create_user
from flask import (
    Blueprint,
    render_template,
    abort,
    request,
    url_for,
    redirect,
)
from blog.posts import (
    get_all_posts,
    get_post_by_slug,
    new_post,
    update_post_by_slug,
)

bp = Blueprint("post", __name__, template_folder="templates")


@bp.route("/")
def index():
    posts = get_all_posts()
    return render_template("index.html.j2", posts=posts)


@bp.route("/new", methods=["GET", "POST"])
@login_required()
def new():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        slug = new_post(title, content)
        return redirect(url_for("post.detail", slug=slug))
    return render_template("form.html.j2")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        create_user(user, password)
        return redirect(url_for("post.index"))
    return render_template("register.html.j2")


@bp.route("/<slug>")
def detail(slug):
    post = get_post_by_slug(slug)
    if not post:
        return abort(404, "Post Not Found")
    return render_template("post.html.j2", post=post)


@bp.route("/<slug>/update", methods=["GET", "POST"])
@login_required()
def update(slug):
    post = get_post_by_slug(slug)
    if not post:
        return abort(404, "Post Not Found")
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        data = {"title": title, "content": content}
        new_slug = slugify(title)
        update_post_by_slug(slug, data)
        return redirect(url_for("post.detail", slug=new_slug))

    return render_template("update.html.j2", post=post)


def configure(app):
    app.register_blueprint(bp)

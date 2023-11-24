import click

from blog.posts import (
    new_post,
    update_post_by_slug,
    delete_post_by_slug,
    get_all_posts,
    get_post_by_slug,
)


@click.group()
def post():
    """Manage blog posts."""


@post.command()
@click.option("--title")
@click.option("--content")
def new(title, content):
    """ Add new post to database"""
    new = new_post(title, content)
    click.echo(f"Post {new} has been created!")


@post.command("list")
def _list():
    """ List all posts"""
    for post in get_all_posts():
        click.echo(post)
        click.echo("~" * 30)


@post.command()
@click.argument("slug")
def get(slug):
    """Get post by slug"""
    click.echo(get_post_by_slug(slug))


@post.command()
@click.argument("slug")
def delete(slug):
    """Delete post by slug"""
    post = delete_post_by_slug(slug)
    click.echo(f"Post {post} has been deleted!")


@post.command()
@click.argument("slug")
@click.option("--content", default=None, type=str)
@click.option("--published", default=None, type=str)
def update(slug, content, published):
    """Update post by slug"""
    data = {}
    if content is not None:
        data["content"] = content
    if published is not None:
        data["published"] = published
    update_post_by_slug(slug, data)
    click.echo("Post updated!")


def configure(app):
    app.cli.add_command(post)

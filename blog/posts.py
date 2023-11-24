from blog.database import mongo
from datetime import datetime
from slugify import slugify


def get_all_posts(published: bool = True):
    posts = mongo.db.posts.find({"published": published})
    return posts.sort("-date")


def get_post_by_slug(slug: str):
    post = mongo.db.posts.find_one({"slug": slug})
    return post


def update_post_by_slug(slug: str, data: dict) -> dict:
    if "title" in data and data["title"] != get_post_by_slug(slug).get(
        "title"
    ):
        data["slug"] = slugify(data["title"])
    return mongo.db.posts.find_one_and_update({"slug": slug}, {"$set": data})


def delete_post_by_slug(slug: str):
    return mongo.db.posts.find_one_and_delete({"slug": slug})


def new_post(title: str, content: str, published: bool = True):
    slug = slugify(title)
    existent_slug = mongo.db.posts.find_one({"slug": slug}).get(slug)
    if slug == existent_slug:
        print("Title already exist!")
    else:
        mongo.db.posts.insert_one(
            {
                "title": title,
                "content": content,
                "published": published,
                "slug": slug,
                "date": datetime.now(),
            }
        )

    return slug

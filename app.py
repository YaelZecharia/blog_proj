from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)


@app.route('/')
def index():
    with open("storage.json", "r") as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        with open('storage.json', 'r') as file:
            blog_posts = json.load(file)

        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        if len(blog_posts) > 0:
            last_post = blog_posts[-1]
            last_post_id = last_post["id"]
            post_id = last_post_id + 1
        else:
            post_id = 1

        new_post = {
            "id": post_id,
            "author": author,
            "title": title,
            "content": content
        }
        blog_posts.append(new_post)

        with open('storage.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<post_id>')
def delete(post_id):
    post_id = int(post_id)
    with open('storage.json', 'r') as file:
        blog_posts = json.load(file)
    for post in range(len(blog_posts)):
        if blog_posts[post]['id'] == post_id:
            del blog_posts[post]
            break

    with open('storage.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    pass


if __name__ == '__main__':
    app.run()

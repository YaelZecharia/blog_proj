from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


# Route to display the index page
@app.route('/')
def index():
    with open("storage.json", "r") as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


# Route to add a new blog post
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        with open('storage.json', 'r') as file:
            blog_posts = json.load(file)

        # Get data from the form
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        # Create a new post ID
        if len(blog_posts) > 0:
            last_post = blog_posts[-1]
            last_post_id = last_post["id"]
            post_id = last_post_id + 1
        else:
            post_id = 1

        # Create a new post dictionary
        new_post = {
            "id": post_id,
            "author": author,
            "title": title,
            "content": content
        }
        # Add the new post to the list
        blog_posts.append(new_post)

        with open('storage.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


# Route to delete a blog post
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


# Route to update a blog post
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    with open('storage.json', 'r') as file:
        blog_posts = json.load(file)

    post = None
    for blog_post in blog_posts:
        if blog_post['id'] == post_id:
            post = blog_post
            break
    if post is None:
        return "post not found", 404
    if request.method == 'POST':
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']

        # Update the post in the JSON file
        with open('storage.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

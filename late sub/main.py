from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Sample data storage (in-memory for simplicity)
users = {}
posts = {}

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

# Create User
@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        abort(400)
    user_id = len(users) + 1
    users[user_id] = {"id": user_id, "name": data["name"], "email": data["email"]}
    return jsonify(users[user_id]), 201

# Get Users
@app.route("/get-users", methods=["GET"])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    name_filter = request.args.get('name', None)

    # Filter users based on the name if provided
    filtered_users = [user for user in users.values() if name_filter.lower() in user['name'].lower()] if name_filter else list(users.values())

    # Pagination logic
    total = len(filtered_users)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = filtered_users[start:end]

    return jsonify({"total": total, "users": paginated_users}), 200

# Get User by ID
@app.route("/get-user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user), 200

# Update User
@app.route("/update-user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = users.get(user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    user.update(data)
    return jsonify(user), 200

# Delete User
@app.route("/delete-user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = users.pop(user_id, None)
    if user is None:
        abort(404)
    return jsonify({"message": "User deleted"}), 204

# Post Endpoints
@app.route("/get-user-posts/<int:user_id>", methods=["GET"])
def get_user_posts(user_id):
    user_posts = posts.get(user_id, [])
    return jsonify(user_posts), 200

@app.route("/create-user-post/<int:user_id>", methods=["POST"])
def create_user_post(user_id):
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        abort(400)
    post_id = len(posts.get(user_id, [])) + 1
    post = {"id": post_id, "title": data["title"], "content": data["content"]}
    
    if user_id not in posts:
        posts[user_id] = []
    posts[user_id].append(post)
    
    return jsonify(post), 201

@app.route("/delete-user-post/<int:user_id>/<int:post_id>", methods=["DELETE"])
def delete_user_post(user_id, post_id):
    user_posts = posts.get(user_id, [])
    post = next((p for p in user_posts if p['id'] == post_id), None)
    if post is None:
        abort(404)
    user_posts.remove(post)
    return jsonify({"message": "Post deleted"}), 204

if __name__ == "__main__":
    app.run(debug=True)
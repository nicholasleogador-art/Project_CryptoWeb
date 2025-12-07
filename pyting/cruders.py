import uuid
from flask import Flask, request, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)

# In-memory "Database" (list of dictionaries)
# This will reset every time the server restarts, but works for a crude example.
DATABASE = []
next_id = 1

# --- Utility Functions for CRUD Operations ---

def get_all_items():
    """Reads all items from the database."""
    # We return a copy to avoid external modification issues, though not strictly necessary here.
    return sorted(DATABASE, key=lambda x: x['id'], reverse=True)

def create_item(name, description):
    """Creates a new item and adds it to the database."""
    global next_id
    new_item = {
        'id': next_id,
        'name': name,
        'description': description
    }
    DATABASE.append(new_item)
    next_id += 1
    return new_item

def get_item_by_id(item_id):
    """Retrieves a single item by its ID."""
    return next((item for item in DATABASE if item['id'] == item_id), None)

def update_item_by_id(item_id, new_name, new_description):
    """Updates an existing item's name and description."""
    item = get_item_by_id(item_id)
    if item:
        item['name'] = new_name
        item['description'] = new_description
        return True
    return False

def delete_item_by_id(item_id):
    """Deletes an item from the database by its ID."""
    global DATABASE
    initial_length = len(DATABASE)
    # Filter out the item to be deleted
    DATABASE = [item for item in DATABASE if item['id'] != item_id]
    return len(DATABASE) < initial_length # True if an item was deleted

# --- HTML Template (Embedded for single-file simplicity) ---

BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crude Flask CRUD App</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        input[type="text"], textarea {{ width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }}
        button {{ padding: 10px 15px; background-color: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        button:hover {{ background-color: #2980b9; }}
        .item-list {{ margin-top: 30px; }}
        .item-card {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 4px; }}
        .item-card h3 {{ margin-top: 0; color: #e74c3c; }}
        .actions a {{ margin-right: 10px; text-decoration: none; color: #2980b9; }}
        .actions form {{ display: inline; }}
    </style>
</head>
<body>
    {content}
</body>
</html>
"""

# --- Flask Routes (Backend + Frontend Rendering) ---

@app.route('/', methods=['GET'])
def index():
    """
    QUERY/READ Route: Displays the submission form (CREATE) and the list of current items (READ).
    """
    items = get_all_items()
    item_list_html = ""

    if not items:
        item_list_html = "<p>No items found. Submit one above!</p>"
    else:
        for item in items:
            item_list_html += f"""
            <div class="item-card">
                <h3>ID: {item['id']} | {item['name']}</h3>
                <p>Description: {item['description']}</p>
                <div class="actions">
                    <a href="{url_for('edit_item', item_id=item['id'])}">Edit (Update)</a>
                    <form method="POST" action="{url_for('delete_item', item_id=item['id'])}" onsubmit="return confirm('Are you sure you want to delete this item?');">
                        <button type="submit">Delete</button>
                    </form>
                </div>
            </div>
            """

    content = f"""
    <h1>Crude Flask CRUD Application</h1>

    <!-- SUBMIT/CREATE FORM -->
    <h2>1. Submit New Item (Create)</h2>
    <form method="POST" action="{url_for('submit_item')}">
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div class="form-group">
            <label for="description">Description:</label>
            <textarea id="description" name="description" rows="3" required></textarea>
        </div>
        <button type="submit">Submit (Create)</button>
    </form>

    <!-- QUERY/READ LIST -->
    <h2>2. Current Items (Query/Read)</h2>
    <div class="item-list">
        {item_list_html}
    </div>
    """
    return BASE_HTML.format(content=content)

@app.route('/submit', methods=['POST'])
def submit_item():
    """SUBMIT/CREATE Route: Handles the form submission."""
    name = request.form.get('name')
    description = request.form.get('description')
    if name and description:
        create_item(name, description)
    return redirect(url_for('index'))

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """UPDATE Route: Displays the edit form (GET) or handles the update (POST)."""
    item = get_item_by_id(item_id)
    if not item:
        return BASE_HTML.format(content=f"<h1>Error</h1><p>Item with ID {item_id} not found.</p>"), 404

    if request.method == 'POST':
        # Handle the form submission for update
        new_name = request.form.get('name')
        new_description = request.form.get('description')
        if new_name and new_description:
            update_item_by_id(item_id, new_name, new_description)
            return redirect(url_for('index'))
        else:
            # Re-render form with error or keep old data
            pass

    # Display the edit form (GET request)
    content = f"""
    <h1>Update Item (ID: {item_id})</h1>
    <form method="POST" action="{url_for('edit_item', item_id=item_id)}">
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" value="{item['name']}" required>
        </div>
        <div class="form-group">
            <label for="description">Description:</label>
            <textarea id="description" name="description" rows="3" required>{item['description']}</textarea>
        </div>
        <button type="submit">Save Changes (Update)</button>
        <a href="{url_for('index')}" style="margin-left: 10px;">Cancel</a>
    </form>
    """
    return BASE_HTML.format(content=content)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    """DELETE Route: Handles the deletion of an item."""
    delete_item_by_id(item_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Add some initial mock data for testing
    create_item("First Project", "Initial setup and database design.")
    create_item("Second Project", "User authentication module implementation.")
    # Run the application
    # Note: Flask will inform you of the URL (e.g., http://127.0.0.1:5000/)
    app.run(debug=True)
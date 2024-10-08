from flask import Flask, request, render_template,jsonify
# app
app = Flask(__name__)
# Store chats in memory (or use a database for persistence in production)
chats = [{'name': 'New Chat', 'id': 1, 'messages': []}]  # Default first chat
# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/get_chats",methods=['GET'])
def get_chats():
    return jsonify({'chats':chats})

@app.route("/get_chat_history",methods=['GET'])
def get_chat_history():
    chat_id = int(request.args.get('chat_id'))
    chat = next((chat for chat in chats if chat['id']==chat_id),None)
    if chat:
        return jsonify({'messages': chat['messages']})
    return jsonify({'messages':[]})

# Route to create a new chat
@app.route('/new_chat', methods=['POST'])
def new_chat():
    data = request.get_json()
    chat_name = data.get('chat_name')
    new_chat_id = len(chats) + 1
    new_chat = {'name': chat_name, 'id': new_chat_id, 'messages': []}
    chats.append(new_chat)
    return jsonify({'status': 'Chat created successfully', 'chat_id': new_chat_id})

# Route to delete a chat
@app.route('/delete_chat', methods=['POST'])
def delete_chat():
    data = request.get_json()
    chat_id = data.get('chat_id')
    global chats
    chats = [chat for chat in chats if chat['id'] != chat_id]
    return jsonify({'status': f'Chat {chat_id} deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

# GET /messages - return all messages ordered by created_at ASC
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([msg.to_dict() for msg in messages]), 200

# POST /messages - create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    try:
        new_msg = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_msg)
        db.session.commit()
        return jsonify(new_msg.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# PATCH /messages/<id> - update message body
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    msg = Message.query.get_or_404(id)
    data = request.get_json()

    if 'body' in data:
        msg.body = data['body']
        db.session.commit()
        return jsonify(msg.to_dict()), 200
    return jsonify({'error': 'No valid fields to update'}), 400

# DELETE /messages/<id> - delete message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return {}, 204

if __name__ == '__main__':
    app.run(port=5555)

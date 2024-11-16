from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging, firestore

app = Flask(__name__)

# Load Firebase credentials
cred = credentials.Certificate("auth/whizsoft-40a69-firebase-adminsdk-5abjw-dc134c45d2.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

@app.route('/send-notification', methods=['POST'])
def send_notification():
    try:
        # Parse the JSON request
        data = request.get_json()
        username = data.get('username')  # Username (uid) to fetch the token
        title = data.get('title', 'Default Title')  # Notification title
        body = data.get('body', 'Default Body')  # Notification body

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # Query the Firestore users collection to find the user by uid
        users_ref = db.collection('users')
        query = users_ref.where('uid', '==', username).limit(1).get()

        if not query:
            return jsonify({'error': f'No user found for username: {username}'}), 404

        # Extract the FCM token from the query result
        user_data = query[0].to_dict()
        token = user_data.get('fcmToken')

        if not token:
            return jsonify({'error': f'No FCM token found for username: {username}'}), 404

        # Create the message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )

        # Send the message via FCM
        response = messaging.send(message)

        return jsonify({'success': True, 'message_id': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

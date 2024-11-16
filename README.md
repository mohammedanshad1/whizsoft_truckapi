
# Firebase Notification Sender API

This Flask application allows sending push notifications via Firebase Cloud Messaging (FCM). It retrieves user FCM tokens stored in a Firestore database and sends notifications to the respective devices.

---

## Features
- Retrieve user FCM tokens from Firestore.
- Send push notifications with customizable titles and bodies.
- Simple and easy-to-use REST API.

---

## Prerequisites

1. **Firebase Project Setup**:
   - Create a Firebase project in the [Firebase Console](https://console.firebase.google.com/).
   - Set up Firestore and add a `users` collection with documents containing `uid` (username) and `fcmToken` fields.

2. **Service Account Key**:
   - Download the Firebase Admin SDK private key:
     - Go to **Project Settings > Service Accounts**.
     - Click **Generate New Private Key**.
     - Save the file as `auth/whizsoft-40a69-firebase-adminsdk-5abjw-dc134c45d2.json`.

3. **Install Python and Dependencies**:
   - Python version: >= 3.7
   - Install dependencies using `pip install -r requirements.txt`.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/firebase-notification-sender.git
   cd firebase-notification-sender
   ```

2. **Set Up the Environment**:
   - Ensure the service account key is saved in the `auth/` directory.
   - Verify the file path in the code:
     ```python
     cred = credentials.Certificate("auth/whizsoft-40a69-firebase-adminsdk-5abjw-dc134c45d2.json")
     ```

3. **Install Required Libraries**:
   ```bash
   pip install flask firebase-admin
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```
   The app will run on `http://127.0.0.1:5000`.

---

## API Endpoint

### **POST** `/send-notification`

#### **Request**
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (JSON):
  ```json
  {
      "username": "user123",
      "title": "Hello!",
      "body": "This is a test notification."
  }
  ```

#### **Response**
- **Success**:
  ```json
  {
      "success": true,
      "message_id": "messageId123"
  }
  ```
- **Error**:
  - Missing `username`:
    ```json
    {
        "error": "Username is required"
    }
    ```
  - User not found:
    ```json
    {
        "error": "No user found for username: user123"
    }
    ```
  - FCM token missing:
    ```json
    {
        "error": "No FCM token found for username: user123"
    }
    ```

---

## Firestore Database Structure

- **Collection**: `users`
  - **Document Fields**:
    - `uid`: Unique identifier for the user.
    - `fcmToken`: Firebase Cloud Messaging token for the user's device.

Example:
```plaintext
users/
  user123/
    uid: "user123"
    fcmToken: "abc123token"
```

---


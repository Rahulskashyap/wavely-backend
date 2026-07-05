from firebase_admin import messaging
from firebase_service import db


def send_podcast_ready_notification(uid):

    user_ref = db.collection("users").document(uid)
    user_data = user_ref.get()

    if not user_data.exists:
        print("NOTIFICATION SKIPPED: User document not found")
        return

    user = user_data.to_dict()

    fcm_token = user.get("fcmToken")

    if not fcm_token:
        print("NOTIFICATION SKIPPED: No FCM token for user", uid)
        return

    message = messaging.Message(
        notification=messaging.Notification(
            title="🎙 Morning Brief Ready",
            body="Your personalized AI podcast is ready to play.",
        ),
        token=fcm_token,
    )

    try:
        response = messaging.send(message)

        print("PUSH NOTIFICATION SENT")
        print("FCM RESPONSE:", response)

    except Exception as e:
        print("PUSH NOTIFICATION FAILED:", str(e))
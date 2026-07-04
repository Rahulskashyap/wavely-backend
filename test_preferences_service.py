from preferences_service import (
    get_user_preferences,
    update_user_preferences
)

print("Before Update:")
print(get_user_preferences(1))

update_user_preferences(
    1,
    "Karnataka",
    "English",
    "India",
    "Female",
    20
)

print("\nAfter Update:")
print(get_user_preferences(1))
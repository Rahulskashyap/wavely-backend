from preferences_service import get_user_preferences


uid = "R2V7CIxEKNVq3TSb94xgNvw91K32"


preferences = get_user_preferences(uid)


print()
print("USER DOCUMENT CREATED")
print("Preferences:", preferences)
from storage_service import upload_podcast_audio

result = upload_podcast_audio(
    file_path="podcasts/R2V7CIxEKNVq3TSb94xgNvw91K32/2026-07-04_final.mp3",
    uid="R2V7CIxEKNVq3TSb94xgNvw91K32",
    date="2026-07-04",
)

print(result)
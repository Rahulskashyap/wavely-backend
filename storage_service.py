import os

import cloudinary
import cloudinary.uploader

from dotenv import load_dotenv

load_dotenv()



cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload_podcast_audio(file_path, uid, date):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Podcast file does not exist: {file_path}"
        )

    print("Uploading podcast to Cloudinary...")

    public_id = f"wavely/podcasts/{uid}/{date}"

    result = cloudinary.uploader.upload(
        file_path,
        resource_type="video",
        public_id=public_id,
        overwrite=True,
    )

    audio_url = result.get("secure_url")

    if not audio_url:
        raise RuntimeError(
            "Cloudinary upload succeeded but no secure URL was returned."
        )

    print("Podcast uploaded successfully.")
    print("Cloudinary URL:", audio_url)

    return {
        "audio_url": audio_url,
        "public_id": result.get("public_id"),
    }


def delete_podcast_audio(public_id):

    if not public_id:
        return

    try:

        cloudinary.uploader.destroy(
            public_id,
            resource_type="video",
        )

        print(
            "Cloudinary podcast deleted:",
            public_id,
        )

    except Exception as e:

        print(
            "Cloudinary delete failed:",
            e,
        )
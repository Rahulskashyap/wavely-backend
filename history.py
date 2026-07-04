import os

podcast_folder = "../podcasts"

files = os.listdir(podcast_folder)

print("\n🎙 PODCAST HISTORY\n")

for file in sorted(files, reverse=True):
    print(file)
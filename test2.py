import os

directory = r"C:\languages\DocLogic\media\videos\29da070f-f454-4853-807e-bdaabf1a991f\480p15"

# List all .mp4 files
mp4_files = [f for f in os.listdir(directory) if f.lower().endswith(".mp4")]

print(mp4_files[0])

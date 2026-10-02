import os


def accept_audio_folder(dir_path):

    valid_extensions = (
        '.mp3',
        '.wav',
        '.flac',
        '.m4a',
        '.ogg',
        '.aac',
        '.wma'
    )

    if not os.path.exists(dir_path):
        print("❌ Error: That folder path does not exist.")
        return None

    if not os.path.isdir(dir_path):
        print("❌ Error: That path points to a file, not a directory.")
        return None

    audio_files = [
        os.path.join(dir_path, file)
        for file in os.listdir(dir_path)
        if file.lower().endswith(valid_extensions)
    ]

    if not audio_files:
        print("⚠️ No supported audio files were found.")
        return None

    print(f"\n✅ Found {len(audio_files)} audio file(s):")

    for file_path in audio_files:
        print(f"   • {os.path.basename(file_path)}")

    return audio_files

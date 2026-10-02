import csv
import os


def delete_duplicates_in_folder(audio_files, csv_path):

    if not os.path.exists(csv_path):
        print(f"❌ Error: CSV file not found at '{csv_path}'.")
        return

    print(f"📖 Loading and indexing CSV ({csv_path})...")

    file_to_hash = {}

    with open(
        csv_path,
        mode='r',
        encoding='utf-8',
        errors='ignore'
    ) as f:

        reader = csv.reader(f)

        try:
            header = next(reader)
        except StopIteration:
            print("❌ Error: CSV file is empty.")
            return

        header_clean = [
            col.strip().lower()
            for col in header
        ]

        try:
            name_idx = header_clean.index('file_name')
            hash_idx = header_clean.index('md5hash')
        except ValueError:
            print(
                "❌ Error: Could not find "
                "'file_name' or 'md5hash' columns."
            )
            return

        for row in reader:

            if len(row) > max(name_idx, hash_idx):

                f_name = row[name_idx].strip()
                f_hash = row[hash_idx].strip()

                if f_name and f_hash:
                    file_to_hash[f_name] = f_hash
                    file_to_hash[os.path.basename(f_name)] = f_hash

    print(
        f"✅ Indexed {len(file_to_hash)} "
        "file lookup keys from CSV."
    )

    seen_hashes = set()
    duplicates_to_delete = []
    missing_count = 0

    for file_path in audio_files:

        base_name = os.path.basename(file_path)

        file_hash = (
            file_to_hash.get(file_path)
            or file_to_hash.get(base_name)
        )

        if not file_hash:
            missing_count += 1
            continue

        if file_hash in seen_hashes:
            duplicates_to_delete.append(file_path)
        else:
            seen_hashes.add(file_hash)

    if missing_count > 0:
        print(
            f"⚠️ Warning: {missing_count} "
            "audio file(s) were not found in CSV."
        )

    if not duplicates_to_delete:
        print("✅ No duplicate audio files detected.")
        return

    print(
        f"\n⚠️ Found {len(duplicates_to_delete)} "
        "duplicate file(s):"
    )

    for path in duplicates_to_delete[:10]:
        print(f"   • {os.path.basename(path)}")

    if len(duplicates_to_delete) > 10:
        print(
            f"   ... and "
            f"{len(duplicates_to_delete) - 10} more."
        )

    confirm = input(
        f"\nDelete these {len(duplicates_to_delete)} "
        "duplicate audio files? (y/n): "
    ).strip().lower()

    if confirm != 'y':
        print("\nNo files deleted.")
        return

    deleted_count = 0

    for path in duplicates_to_delete:

        try:
            os.remove(path)
            deleted_count += 1

        except OSError as e:
            print(
                f"❌ Error deleting "
                f"{os.path.basename(path)}: {e}"
            )

    print(
        f"\n✅ Cleanup completed. "
        f"Deleted {deleted_count} file(s)."
    )

from Input_songs import accept_audio_folder
from delete_duplicates import delete_duplicates_in_folder


def main():

    print("=== Audio Directory Processing Script ===")

    dir_path = input(
        "\nPlease enter the path to your audio folder: "
    ).strip().strip('\'"')

    audio_files = accept_audio_folder(dir_path)

    if audio_files is None:
        return

    csv_path = input(
        "\nPlease enter the path to the CSV file: "
    ).strip().strip('\'"')

    delete_duplicates_in_folder(
        audio_files,
        csv_path
    )


if __name__ == "__main__":
    main()

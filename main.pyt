import os

print("==============================")
print("      AI FILE DETECTIVE")
print("==============================")

folder_path = input("Enter folder path: ")

if not os.path.exists(folder_path):
    print("Folder does not exist!")

else:

    image_count = 0
    video_count = 0
    document_count = 0
    python_count = 0
    other_count = 0
    total_size = 0

    for root, folders, files in os.walk(folder_path):

        for file in files:

            file_path = os.path.join(root, file)

            # Get file size safely
            try:
                total_size += os.path.getsize(file_path)
            except (FileNotFoundError, PermissionError):
                continue

            extension = os.path.splitext(file)[1].lower()

            # Classify files
            if extension in [".jpg", ".jpeg", ".png", ".gif", ".avif", ".webp"]:
                image_count += 1

            elif extension in [".mp4", ".mkv", ".avi", ".mov", ".webm"]:
                video_count += 1

            elif extension in [".pdf", ".docx", ".txt", ".pptx", ".xlsx", ".csv"]:
                document_count += 1

            elif extension == ".py":
                python_count += 1

            else:
                other_count += 1

    total_files = (
        image_count
        + video_count
        + document_count
        + python_count
        + other_count
    )

    print("\n===== SCAN RESULT =====")

    print("Files scanned:", total_files)
    print("Images:", image_count)
    print("Videos:", video_count)
    print("Documents:", document_count)
    print("Python files:", python_count)
    print("Other files:", other_count)

    total_size_mb = total_size / (1024 * 1024)

    print("Total size:", round(total_size_mb, 2), "MB")

    print("\n==============================")
    print("       SCAN COMPLETED")
    print("==============================")

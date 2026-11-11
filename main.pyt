import os
import hashlib

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

    # Store files grouped by their size
    file_sizes = {}

    duplicate_count = 0
    duplicate_size = 0

    # ------------------------------
    # STEP 1: SCAN ALL FILES
    # ------------------------------

    print("\nScanning files...")

    for root, folders, files in os.walk(folder_path):

        for file in files:

            file_path = os.path.join(root, file)

            try:
                file_size = os.path.getsize(file_path)
            except (FileNotFoundError, PermissionError):
                continue

            total_size += file_size

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

            # Store file according to its size
            if file_size not in file_sizes:
                file_sizes[file_size] = []

            file_sizes[file_size].append(file_path)

    # ------------------------------
    # STEP 2: FIND POSSIBLE DUPLICATES
    # ------------------------------

    print("Checking for duplicate files...")

    for file_size, files in file_sizes.items():

        # If only one file has this size,
        # it cannot be a duplicate of another file.
        if len(files) < 2:
            continue

        hashes = {}

        # ------------------------------
        # STEP 3: HASH SAME-SIZE FILES
        # ------------------------------

        for file_path in files:

            try:

                hash_object = hashlib.sha256()

                with open(file_path, "rb") as f:

                    while True:

                        chunk = f.read(1024 * 1024)

                        if not chunk:
                            break

                        hash_object.update(chunk)

                file_hash = hash_object.hexdigest()

            except (FileNotFoundError, PermissionError):
                continue

            # ------------------------------
            # STEP 4: CHECK HASH
            # ------------------------------

            if file_hash in hashes:

                duplicate_count += 1
                duplicate_size += file_size

                print("\nDUPLICATE FOUND!")

                print("Original:", hashes[file_hash])

                print("Duplicate:", file_path)

                print(
                    "Size:",
                    round(file_size / (1024 * 1024), 2),
                    "MB"
                )

            else:

                hashes[file_hash] = file_path

    # ------------------------------
    # FINAL RESULTS
    # ------------------------------

    total_files = (
        image_count
        + video_count
        + document_count
        + python_count
        + other_count
    )

    total_size_mb = total_size / (1024 * 1024)

    duplicate_size_mb = duplicate_size / (1024 * 1024)

    print("\n==============================")
    print("       SCAN RESULT")
    print("==============================")

    print("Files scanned:", total_files)
    print("Images:", image_count)
    print("Videos:", video_count)
    print("Documents:", document_count)
    print("Python files:", python_count)
    print("Other files:", other_count)

    print("\nTotal size:", round(total_size_mb, 2), "MB")

    print("\n==============================")
    print("    DUPLICATE FILE RESULT")
    print("==============================")

    print("Duplicate files:", duplicate_count)

    print(
        "Duplicate storage:",
        round(duplicate_size_mb, 2),
        "MB"
    )

    print("\n==============================")
    print("       SCAN COMPLETED")
    print("==============================")
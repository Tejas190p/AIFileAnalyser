import os
import hashlib
from datetime import datetime, timedelta

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

    image_size = 0
    video_size = 0
    document_size = 0
    python_size = 0
    other_size = 0

    total_size = 0

    # Store files grouped by their size
    file_sizes = {}

    duplicate_count = 0
    duplicate_size = 0

    # Day 3: Large and old files
    largest_files = []
    old_files = []

    # 30 days ago
    old_file_date = datetime.now() - timedelta(days=30)

    # ------------------------------
    # STEP 1: SCAN ALL FILES
    # ------------------------------

    print("\nScanning files...")

    for root, folders, files in os.walk(folder_path):

        for file in files:

            file_path = os.path.join(root, file)

            try:
                file_size = os.path.getsize(file_path)
                modified_time = os.path.getmtime(file_path)

            except (FileNotFoundError, PermissionError):
                continue

            total_size += file_size

            extension = os.path.splitext(file)[1].lower()

            # ------------------------------
            # CLASSIFY FILES
            # ------------------------------

            if extension in [
                ".jpg", ".jpeg", ".png",
                ".gif", ".avif", ".webp"
            ]:
                image_count += 1
                image_size += file_size

            elif extension in [
                ".mp4", ".mkv", ".avi",
                ".mov", ".webm"
            ]:
                video_count += 1
                video_size += file_size

            elif extension in [
                ".pdf", ".docx", ".txt",
                ".pptx", ".xlsx", ".csv"
            ]:
                document_count += 1
                document_size += file_size

            elif extension == ".py":
                python_count += 1
                python_size += file_size

            else:
                other_count += 1
                other_size += file_size

            # ------------------------------
            # STORE FILE BY SIZE
            # ------------------------------

            if file_size not in file_sizes:
                file_sizes[file_size] = []

            file_sizes[file_size].append(file_path)

            # ------------------------------
            # DAY 3: LARGE FILES
            # ------------------------------

            largest_files.append(
                (file_size, file_path)
            )

            # ------------------------------
            # DAY 3: OLD FILES
            # ------------------------------

            modified_date = datetime.fromtimestamp(
                modified_time
            )

            if modified_date < old_file_date:

                old_files.append(
                    (modified_date, file_size, file_path)
                )

    # ------------------------------
    # STEP 2: FIND DUPLICATES
    # ------------------------------

    print("Checking for duplicate files...")

    for file_size, files in file_sizes.items():

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

                print(
                    "Original:",
                    hashes[file_hash]
                )

                print(
                    "Duplicate:",
                    file_path
                )

                print(
                    "Size:",
                    round(
                        file_size / (1024 * 1024),
                        2
                    ),
                    "MB"
                )

            else:

                hashes[file_hash] = file_path

    # ------------------------------
    # DAY 3: SORT FILES
    # ------------------------------

    # Largest files first
    largest_files.sort(reverse=True)

    # Oldest files first
    old_files.sort()

    # ------------------------------
    # FINAL CALCULATIONS
    # ------------------------------

    total_files = (
        image_count
        + video_count
        + document_count
        + python_count
        + other_count
    )

    total_size_mb = total_size / (1024 * 1024)

    duplicate_size_mb = (
        duplicate_size / (1024 * 1024)
    )

    # ------------------------------
    # SCAN RESULT
    # ------------------------------

    print("\n==============================")
    print("       SCAN RESULT")
    print("==============================")

    print(
        "Files scanned:",
        total_files
    )

    print(
        "Images:",
        image_count
    )

    print(
        "Videos:",
        video_count
    )

    print(
        "Documents:",
        document_count
    )

    print(
        "Python files:",
        python_count
    )

    print(
        "Other files:",
        other_count
    )

    print(
        "\nTotal size:",
        round(total_size_mb, 2),
        "MB"
    )

    # ------------------------------
    # DUPLICATE RESULTS
    # ------------------------------

    print("\n==============================")
    print("    DUPLICATE FILE RESULT")
    print("==============================")

    print(
        "Duplicate files:",
        duplicate_count
    )

    print(
        "Duplicate storage:",
        round(
            duplicate_size_mb,
            2
        ),
        "MB"
    )

    # ------------------------------
    # TOP 10 LARGEST FILES
    # ------------------------------

    print("\n==============================")
    print("       TOP 10 LARGEST FILES")
    print("==============================")

    for size, path in largest_files[:10]:

        print(
            "\nFile:",
            os.path.basename(path)
        )

        print(
            "Size:",
            round(
                size / (1024 * 1024),
                2
            ),
            "MB"
        )

        print(
            "Path:",
            path
        )

    # ------------------------------
    # OLD FILES
    # ------------------------------

    print("\n==============================")
    print("       OLD FILES (30+ DAYS)")
    print("==============================")

    print(
        "Old files found:",
        len(old_files)
    )

    for modified_date, size, path in old_files[:10]:

        print(
            "\nFile:",
            os.path.basename(path)
        )

        print(
            "Last modified:",
            modified_date.strftime(
                "%Y-%m-%d"
            )
        )

        print(
            "Size:",
            round(
                size / (1024 * 1024),
                2
            ),
            "MB"
        )

        print(
            "Path:",
            path
        )

    # ------------------------------
    # DAY 4: STORAGE ANALYSIS
    # ------------------------------

    categories = {
        "Images": image_size,
        "Videos": video_size,
        "Documents": document_size,
        "Python": python_size,
        "Other": other_size
    }

    print("\n==============================")
    print("       STORAGE ANALYSIS")
    print("==============================")

    for category, size in sorted(
        categories.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        if total_size > 0:
            percentage = (
                size / total_size
            ) * 100
        else:
            percentage = 0

        print(
            category + ":",
            round(
                size / (1024 * 1024),
                2
            ),
            "MB",
            "(",
            round(percentage, 2),
            "%)"
        )

    # ------------------------------
    # DAY 4: SMART ANALYSIS
    # ------------------------------

    print("\n==============================")
    print("       SMART ANALYSIS")
    print("==============================")

    largest_category = max(
        categories,
        key=categories.get
    )

    print(
        "Largest storage category:",
        largest_category
    )

    print(
        "Storage used by it:",
        round(
            categories[largest_category]
            / (1024 * 1024),
            2
        ),
        "MB"
    )

    # ------------------------------
    # DAY 4: RECOMMENDATION
    # ------------------------------

    print("\n==============================")
    print("     STORAGE RECOMMENDATION")
    print("==============================")

    if duplicate_size > 0:

        print(
            "Recommendation:"
        )

        print(
            "Review duplicate files first."
        )

        print(
            "Potential duplicate storage:",
            round(
                duplicate_size_mb,
                2
            ),
            "MB"
        )

    elif largest_category == "Videos":

        print(
            "Recommendation:"
        )

        print(
            "Review large video files first."
        )

    elif largest_category == "Images":

        print(
            "Recommendation:"
        )

        print(
            "Review old and large images."
        )

    elif largest_category == "Documents":

        print(
            "Recommendation:"
        )

        print(
            "Review old documents and unused files."
        )

    else:

        print(
            "Recommendation:"
        )

        print(
            "Review your largest files first."
        )

    # ------------------------------
    # DAY 4: CLEANUP CANDIDATES
    # ------------------------------

    print("\n==============================")
    print("      CLEANUP CANDIDATES")
    print("==============================")

    if duplicate_count > 0:

        print(
            "1. Duplicate files:",
            duplicate_count
        )

    if len(largest_files) > 0:

        largest_size = (
            largest_files[0][0]
            / (1024 * 1024)
        )

        print(
            "2. Largest file:",
            os.path.basename(
                largest_files[0][1]
            ),
            "-",
            round(
                largest_size,
                2
            ),
            "MB"
        )

    if len(old_files) > 0:

        print(
            "3. Old files:",
            len(old_files)
        )

    # ------------------------------
    # COMPLETED
    # ------------------------------

    print("\n==============================")
    print("       SCAN COMPLETED")
    print("==============================")
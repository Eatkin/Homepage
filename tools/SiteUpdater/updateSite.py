import requests
import urllib.parse
import os
import csv

# Constants
CSV_NAME = "file_modified_dates.csv"
CSV_LOCATION = os.path.dirname(os.path.realpath(__file__))
IGNORE_FOLDERS = ["tools", "api_testing"]
IGNORE_FILES = [
    "README.md",
    "comic_data.json",
]


def neocities_init():
    """Gets username and password to construct a URL for uploading files to neocities."""
    # Get the password from the user
    unparsed_password = input("Enter password: ")

    # Parse the password for URL
    password = urllib.parse.quote(unparsed_password, safe="")

    # Prepare URL and request session
    upload_url = f"https://eatkin:{password}@neocities.org/api/upload"

    return upload_url


def get_file_modified_dates():
    file_data = {}
    # Crawl the directory and get the modified dates of all files
    for root, dirs, files in os.walk("."):
        # Check if root is valid - split by os.sep to get the root folder
        try:
            root_folder = root.split(os.sep)[1]
        except:
            root_folder = ""
        if root_folder in IGNORE_FOLDERS or root_folder.startswith("."):
            continue
        for file in files:
            # Ignore any files that start with a dot
            if file.startswith("."):
                continue

            # If the file is in the ignore list, ignore it
            if file in IGNORE_FILES:
                continue

            # Make sure we're not in an ignored folder and make sure the file does not start with a dot
            # Get the modified date
            modified_date = os.path.getmtime(os.path.join(root, file))
            filepath = os.path.join(root, file)
            # Delete the .\ from the filepath
            filepath = filepath[2:]
            # Add to the file_data dictionary
            # Filename is the key and the modified date is the value
            file_data[filepath] = modified_date

    return file_data


def get_previous_file_data():
    # Load the csv into a dictionary of the same form as data dictionary
    old_file_data = {}
    with open(os.path.join(CSV_LOCATION, CSV_NAME), "r") as csvfile:
        csv_dict_reader = csv.DictReader(csvfile)
        for row in csv_dict_reader:
            old_file_data[row["filepath"]] = float(row["modified_date"])

    return old_file_data


def get_file_changes(file_data, old_file_data):
    # Now we can compare the two dictionaries and filter to only include files that have been modified
    files_to_upload = []
    for filepath, modified_date in file_data.items():
        # Trivial - it's a new file
        if filepath not in old_file_data:
            files_to_upload.append(filepath)
            continue

        # Otherwise we need to check if the modified date is different
        if old_file_data[filepath] != modified_date:
            files_to_upload.append(filepath)

    return files_to_upload


def update_file_changes(data, uploads, successful_uploads):
    # Now save the updated file data to the csv
    with open(os.path.join(CSV_LOCATION, CSV_NAME), "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["filepath", "modified_date"])
        for filepath, modified_date in file_data.items():
            # If the upload failed, revert the modified date to the previous one
            if filepath in uploads and filepath not in successful_uploads:
                # If it was unsuccessful BUT it was a new file, we do nothing so it will be uploaded next time
                if filepath not in previous_file_data:
                    continue
                modified_date = previous_file_data[filepath]

            csvwriter.writerow([filepath, modified_date])


def upload_file(filepath, upload_url):
    # Construct the data - replace backslashes with forward slashes otherwise it won't work correctly for folder structure
    files = {filepath.replace("\\", "/"): open(filepath, "rb")}

    # Send the POST request
    response = requests.post(upload_url, files=files)

    success = False

    # Check the response
    if response.status_code == 200:
        print(f"File {filepath} uploaded successfully.")
        success = True
    else:
        print(f"Upload for {filepath} failed with status code:", response.status_code)


def update_site(files_to_upload, upload_url, passthrough=False):
    # Upload each file
    successful_uploads = []

    # Small method if something goes wrong and we want to skip the upload to update the csv
    if passthrough:
        successful_uploads = files_to_upload
        return successful_uploads

    for filepath in files_to_upload:
        success = upload_file(filepath, upload_url)
        if success:
            successful_uploads.append(filepath)

    return successful_uploads


# Get the upload URL
upload_url = neocities_init()

# Get when every file has been modified
file_data = get_file_modified_dates()

# Prior file modified data
previous_file_data = get_previous_file_data()

# Compare to saved data to see if any files have been modified
modified_files = get_file_changes(file_data, previous_file_data)

if modified_files == []:
    print("No changes detected.")
    exit()

print("Files to upload:", "\n".join(modified_files))

if len(modified_files) > 10:
    print(
        "That's a lot of files. Are you sure you want to upload them all? Please manually review the list of files to upload."
    )
    if input("Continue? [y/n]: ") != "y":
        exit()

# Upload the files
successful_uploads = update_site(modified_files, upload_url)

# Update the csv with the new file data
update_file_changes(file_data, modified_files, successful_uploads)

""" There is one thing missing from here - it won't delete files that have been removed from the directory
But that's not a big deal, I can just manually delete them from the site
If it becomes a big deal there's two API access points I can use:
Get all files: https://USER:PASS@neocities.org/api/list
Delete files: curl -d "filenames[]=img1.jpg" -d "filenames[]=img2.jpg" "https://YOURUSER:YOURPASS@neocities.org/api/delete"
There's also no way to cross-reference the files on the site with the files on the computer but that's not a big deal either
"""

import os
import shutil
import glob




def getDownloaded(destinationPath):
# Define the source and destination folders
    downloads_folder = os.path.expanduser('~') + '/Downloads'
    destination_folder = destinationPath

    # Specify the file extension of your archive file (e.g., .zip, .tar.gz, etc.)
    archive_extension = '.zip'

    # Create a list of all archive files in the downloads folder
    archive_files = glob.glob(os.path.join(downloads_folder, f'*{archive_extension}'))

    # Sort the list of archive files by modification time in descending order
    archive_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # Check if there are any archive files
    if archive_files:
        # Get the path of the most recently downloaded archive file
        last_downloaded_archive = archive_files[0]

        # Construct the destination path
        destination_path = os.path.join(destination_folder, os.path.basename(last_downloaded_archive))

        # Move the file to the destination folder
        shutil.move(last_downloaded_archive, destination_path)

        print(f"Moved {last_downloaded_archive} to {destination_path}")
    else:
        print("No archive files found in the downloads folder.")

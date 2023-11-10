import shutil
import sched
import time
import logging
import argparse

def synchronize_folders(source_folder, replica_folder):
    try:
        # Copy files from source to replica (one-way synchronization)
        shutil.rmtree(replica_folder)  # Remove the replica folder and its contents
        shutil.copytree(source_folder, replica_folder)  # Recreate the replica by copying the source
        logging.info("Replica folder updated to match the source folder.")
    except Exception as e:
        logging.error(f"Error during synchronization: {str(e)}")

def sync_periodically(sc, source_folder, replica_folder):
    synchronize_folders(source_folder, replica_folder)
    # Schedule the next synchronization
    s.enter(sync_interval, 1, sync_periodically, (sc, source_folder, replica_folder))

# Set up logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Folder Synchronization")
parser.add_argument("source_folder", help="Path to the source folder")
parser.add_argument("replica_folder", help="Path to the replica folder")
parser.add_argument("--interval", type=int, default=3600, help="Synchronization interval in seconds")
parser.add_argument("--log_file", default="sync_log.txt", help="Path to the log file")
args = parser.parse_args()

source_folder = args.source_folder
replica_folder = args.replica_folder
sync_interval = args.interval
log_file = args.log_file

# Create a scheduler
s = sched.scheduler(time.time, time.sleep)

# Initial synchronization
synchronize_folders(source_folder, replica_folder)

# Start periodic synchronization
s.enter(sync_interval,1,sync_periodically,(s,))
s.run()

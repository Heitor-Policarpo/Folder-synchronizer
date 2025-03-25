import os
import shutil
import time


def get_user_inputs():
    source = input("Enter the source folder path: ").strip()
    replica = input("Enter the replica folder path: ").strip()
    interval = input("Enter synchronization interval in seconds (default: 10): ").strip()
    log_file = input("Enter the log file path (default: sync_log.txt): ").strip()

    interval = int(interval) if interval.isdigit() else 10
    log_file = log_file if log_file else "sync_log.txt"

    return source, replica, interval, log_file


SOURCE_FOLDER, REPLICA_FOLDER, SYNC_INTERVAL, LOG_FILE = get_user_inputs()


def create_folders():
    os.makedirs(SOURCE_FOLDER, exist_ok=True)
    os.makedirs(REPLICA_FOLDER, exist_ok=True)


def create_file(filename):
    file_path = os.path.join(SOURCE_FOLDER, filename)
    with open(file_path, 'w') as file:
        file.write('')
    print(f"File '{filename}' created in {SOURCE_FOLDER}.")


def copy_file(filename):
    source_path = os.path.join(SOURCE_FOLDER, filename)
    replica_path = os.path.join(REPLICA_FOLDER, filename)

    if os.path.exists(source_path):
        shutil.copy2(source_path, replica_path)
        print(f"File '{filename}' copied to {REPLICA_FOLDER}.")
    else:
        print(f"File '{filename}' does not exist in {SOURCE_FOLDER}.")


def delete_file(filename):
    file_path = os.path.join(SOURCE_FOLDER, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{filename}' deleted from {SOURCE_FOLDER}.")
    else:
        print(f"File '{filename}' does not exist in {SOURCE_FOLDER}.")


def sync_folders():
    source_files = set(os.listdir(SOURCE_FOLDER))
    replica_files = set(os.listdir(REPLICA_FOLDER))

    for file in source_files:
        source_path = os.path.join(SOURCE_FOLDER, file)
        replica_path = os.path.join(REPLICA_FOLDER, file)

        if not os.path.exists(replica_path) or (
                os.path.getmtime(source_path) != os.path.getmtime(replica_path)
        ):
            shutil.copy2(source_path, replica_path)
            message = f"File '{file}' synchronized from source to replica."
            print(message)
            log(message)

    for file in replica_files - source_files:
        os.remove(os.path.join(REPLICA_FOLDER, file))
        message = f"File '{file}' removed from replica (no longer in source)."
        print(message)
        log(message)


def log(message):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


def periodic_sync():
    create_folders()
    while True:
        sync_folders()
        log("Folders synchronized.")
        time.sleep(SYNC_INTERVAL)


if __name__ == "__main__":
    periodic_sync()

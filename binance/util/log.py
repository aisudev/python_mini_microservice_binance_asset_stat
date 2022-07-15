from datetime import datetime


# print log info
def log_info(msg: str):
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(f"[INFO - {now}]: {msg}")


# print log error
def log_error(msg: str):
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(f"[ERROR - {now}]: {msg}")


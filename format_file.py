from datetime import datetime


def format_datetime():
    now = datetime.now()  # get datetime
    # format datetime:
    # dd_mm_YY_H_M_S
    # Using _ for Windows file system instead of : or /
    formatted_dt = now.strftime("%d_%m_%Y_%H_%M_%S")
    return formatted_dt

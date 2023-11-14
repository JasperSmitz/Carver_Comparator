import psutil


def check_drive_fragmentation(drive):
    try:
        partitions = psutil.disk_partitions(all=True)
        for partition in partitions:
            if partition.device == drive:
                fragmentation = psutil.disk_usage(partition.mountpoint).percent
                return fragmentation
        return None
    except Exception as e:
        print(f"Error checking fragmentation: {e}")
        return None

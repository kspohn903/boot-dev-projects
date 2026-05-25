def check_mount_rental(time_used, time_leased):
    return "overtime charged" if (time_used >= time_leased) else "no charges yet"


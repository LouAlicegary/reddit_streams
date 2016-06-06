
def log_level(message, level = 1) :
    
    log_string = "=== LOG ===    "
    log_string += ( (level - 1) * 5) * " "
    log_string += message

    print(log_string)

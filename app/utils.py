def get_flash_category(msg):
    if "LỖI" in msg:
        category = "error"
    else:
        category = "success"

    return category

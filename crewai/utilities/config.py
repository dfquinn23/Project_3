def process_config(values, cls):
    # Directly access the 'config' attribute
    return getattr(values, 'config', {})

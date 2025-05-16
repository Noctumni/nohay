# cooldowns.py

cooldowns = {}

def is_on_cooldown(user_id, command, cooldown_time):
    import time
    now = time.time()
    key = f"{user_id}_{command}"
    last_used = cooldowns.get(key, 0)
    if now - last_used < cooldown_time:
        return True, int(cooldown_time - (now - last_used))
    cooldowns[key] = now
    return False, 0

def load_data():
    global cooldowns
    cooldowns = {}  # Reset at each startup, not persisted

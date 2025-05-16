import json
import os

DATA_FILE = "data.json"
data = {}

def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {"users": {}, "shop": {}}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user(user_id):
    uid = str(user_id)
    if uid not in data["users"]:
        data["users"][uid] = {
            "cowoncy": 0,
            "inventory": [],
            "pets": {},
            "xp": 0,
            "level": 1,
            "last_hunt": 0
        }
    return data["users"][uid]

def add_xp(user, amount):
    user["xp"] += amount
    while user["xp"] >= user["level"] * 100:
        user["xp"] -= user["level"] * 100
        user["level"] += 1

def register_commands(bot):
    @bot.command()
    async def level(ctx):
        user = get_user(ctx.author.id)
        await ctx.send(f"You are level {user['level']} with {user['xp']} XP.")

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

def register_commands(bot):
    @bot.command()
    async def inventory(ctx):
        user = get_user(ctx.author.id)
        if not user["inventory"]:
            await ctx.send("Your inventory is empty.")
        else:
            items = {}
            for item in user["inventory"]:
                items[item] = items.get(item, 0) + 1
            msg = "**Your Inventory:**\n"
            for item, count in items.items():
                msg += f"{item} x{count}\n"
            await ctx.send(msg)

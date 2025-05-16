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
    async def pets(ctx):
        user = get_user(ctx.author.id)
        pets = user["pets"]
        if not pets:
            await ctx.send("You don't have any pets yet! Use `owo hunt` to find some.")
            return
        pet_list = "\n".join([f"{p}: {c}" for p, c in pets.items()])
        await ctx.send(f"Your pets:\n{pet_list}")

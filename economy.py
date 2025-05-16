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
    async def balance(ctx):
        user = get_user(ctx.author.id)
        await ctx.send(f"{ctx.author.name}, you have 💴 {user['cowoncy']} cowoncy!")

    @bot.command()
    async def daily(ctx):
        import time
        user = get_user(ctx.author.id)
        now = time.time()
        if "last_daily" in user and now - user["last_daily"] < 86400:
            await ctx.send("You already claimed your daily reward today! Come back tomorrow.")
            return
        reward = 500
        user["cowoncy"] += reward
        user["last_daily"] = now
        save_data()
        await ctx.send(f"You claimed your daily {reward} cowoncy!")


import json
import os
import random
import time

DATA_FILE = "data.json"
data = {}

COOLDOWN_HUNT = 0  # seconds

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
    async def hunt(ctx):
        user = get_user(ctx.author.id)
        now = time.time()
        if now - user["last_hunt"] < COOLDOWN_HUNT:
            left = int(COOLDOWN_HUNT - (now - user["last_hunt"]))
            await ctx.send(f"You're tired! Try hunting again in {left} seconds.")
            return

        rewards = [
            {"type": "cowoncy", "amount": random.randint(20, 100)},
            {"type": "pet", "name": random.choice(["dog", "cat", "fox", "rabbit"])},
            {"type": "cowoncy", "amount": random.randint(10, 50)},
        ]
        reward = random.choice(rewards)

        if reward["type"] == "cowoncy":
            user["cowoncy"] += reward["amount"]
            msg = f"🎯 You hunted and earned 💴 {reward['amount']} cowoncy!"
        else:  # pet reward
            pet = reward["name"]
            pets = user["pets"]
            pets[pet] = pets.get(pet, 0) + 1
            msg = f"🎉 You found a **{pet}** pet! You now have {pets[pet]} of this pet."

        user["last_hunt"] = now
        save_data(data)
        await ctx.send(msg)

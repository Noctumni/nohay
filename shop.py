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
    async def shop(ctx):
        shop_items = data.get("shop", {})
        if not shop_items:
            await ctx.send("The shop is currently empty.")
            return
        msg = "**Shop Items:**\n"
        for item, info in shop_items.items():
            msg += f"**{item}** - 💴 {info['price']} - {info['description']}\n"
        await ctx.send(msg)

    @bot.command()
    async def buy(ctx, item_name: str):
        user = get_user(ctx.author.id)
        shop_items = data.get("shop", {})
        item = shop_items.get(item_name.lower())
        if not item:
            await ctx.send("Item not found in shop!")
            return
        if user["cowoncy"] < item["price"]:
            await ctx.send("You don’t have enough cowoncy to buy that!")
            return
        user["cowoncy"] -= item["price"]
        user["inventory"].append(item_name.lower())
        save_data()
        await ctx.send(f"You bought a {item_name}!")

    @bot.command()
    async def sell(ctx, item_name: str):
        user = get_user(ctx.author.id)
        item_name = item_name.lower()
        if item_name not in user["inventory"]:
            await ctx.send("You don’t have that item in your inventory.")
            return
        shop_items = data.get("shop", {})
        item = shop_items.get(item_name)
        if not item:
            await ctx.send("That item can’t be sold.")
            return
        sell_price = item["price"] // 2
        user["inventory"].remove(item_name)
        user["cowoncy"] += sell_price
        save_data()
        await ctx.send(f"You sold {item_name} for 💴 {sell_price} cowoncy.")

import discord
from discord.ext import commands
import json
import random
import datetime

with open("./data/config.json", 'r+') as f:
  dat1414a = json.load(f)
  ownerids = dat1414a['ownerids']
names = ["Jake Paul", "Random Kid", "Dad", "PoliceMan", "tommhe"]
mainshop = [{"name": "Watch", "price":100, "description": "Time"},
            {"name": "Laptop", "price":1000, "description": "Work"},
            {"name": "PC", "price": 10000, "description": "Gaming"}]
date = datetime.datetime.now()
TodayAtEmbed = f"Today at {date:%I}:{date:%M} {date:%p}"

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break
    if name_ == None:
        return [False,1]
    cost = price*amount
    users = await get_bank_data()
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    
    with open("mainbank.json","w") as f:
        json.dump(users,f)
    await update_bank(user,cost,"wallet")
    return [True,"Worked"]

async def update_bank(user, change = 0, mode="wallet"):
  users = await get_bank_data()
  users[str(user.id)][mode] += change
  with open("./data/mainbank.json", 'w') as f:
    json.dump(users, f)
  bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
  return bal

async def buy_this(user,item_name,amount):
  item_name = item_name.lower()
  name_ = None
  for item in mainshop:
    name = item["name"].lower()
    if name == item_name:
      name_ = name
      price = item["price"]
      break
  if name_ == None:
    return [False,1]
  cost = price*amount
  users = await get_bank_data()
  bal = await update_bank(user)
  if bal[0]<cost:
    return [False,2]
  try:
    index = 0
    t = None
    for thing in users[str(user.id)]["bag"]:
      n = thing["item"]
      if n == item_name:
        old_amt = thing["amount"]
        new_amt = old_amt + amount
        users[str(user.id)]["bag"][index]["amount"] = new_amt
        t = 1
        break
        index+=1 
    if t == None:
      obj = {"item":item_name , "amount" : amount}
      users[str(user.id)]["bag"].append(obj)
  except:
    obj = {"item":item_name , "amount" : amount}
    users[str(user.id)]["bag"] = [obj]        
  with open("mainbank.json","w") as f:
    json.dump(users,f)
  await update_bank(user,cost*-1,"wallet")
  return [True,"Worked"]

async def open_account(user):
  users = await get_bank_data()
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 0
  with open("./data/mainbank.json", 'w') as f:
    json.dump(users, f)
  return True
async def get_bank_data():
  with open("./data/mainbank.json", 'r') as f:
    users = json.load(f)
  return users

class currency(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=["bal"])
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def balance(self, ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    em = discord.Embed(title=f"{ctx.message.author}'s Balance:", color=random.randint(0, 0xFFFFF))
    em.add_field(name=f":money_with_wings: | **__Wallet:__** ", value=f"[`{wallet_amt}`]", inline=False)
    em.add_field(name=":bank: | **__Bank:__** ", value=f"[`{bank_amt}`]", inline=False)
    em.set_thumbnail(url=user.avatar_url)
    em.set_footer(text=TodayAtEmbed)
    await ctx.send(embed=em)

  








  
    



  


  
  @commands.command()
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def sell(self, ctx,item,amount = 1):
    await open_account(ctx.author)
    res = await sell_this(ctx.author,item,amount)
    if not res[0]:
      if res[1]==1:
        em = discord.Embed(title=f":x: That Object isn't there!", color=discord.Color.red())
        em.set_footer(text=TodayAtEmbed)
        await ctx.send()
        return
      if res[1]==2:
        await ctx.send(f"You don't have {amount} {item} in your bag.")
        return
      if res[1]==3:
         await ctx.send(f"You don't have {item} in your bag.")
         return
    await ctx.send(f"You just sold {amount} {item}.")
  
     

  @commands.command(aliases=["leaderboards"])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def rich(self, ctx, x=1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
      name = int(user)
      total_amount = users[user]["wallet"] + users[user]["bank"]
      leader_board[total_amount] = name
      total.append(total_amount)
    total = sorted(total, reverse=True)
    members = ""
    em = discord.Embed(title=f"Top {x} Richest People", color=random.randint(0, 0xFFFFF))
    index = 1
    for amt in total:
      id_ = leader_board[amt]
      member = self.client.get_user(id_)
      name = member
      members += f"**{index}.** __{name}__ - *${amt}*\n"
      if index == x:
        break
      else:
        index += 1
    em.description = members
    em.set_thumbnail(url=ctx.guild.icon_url)
    em.set_footer(text=TodayAtEmbed)
    await ctx.send(embed=em)
    


  @commands.command()
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def buy(self, ctx,item,amount=1):
    await open_account(ctx.author)
    res = await buy_this(ctx.author,item,amount)
    if not res[0]:
      if res[1]==1:
        em = discord.Embed(title=f":x: This object isn't there!", color=discord.Color.red())
        em.set_footer(text=TodayAtEmbed)
        await ctx.send(embed=em)
        return
      if res[1]==2:
        em = discord.Embed(title=f":x: You don't have enough money in your wallet to buy **{amount} {item}**!", color=discord.Color.red())
        em.set_footer(text=TodayAtEmbed)
        await ctx.send(embed=em)
        return
    em = discord.Embed(title=f":white_check_mark: | You just bought **{amount} {item}**!", color=discord.Color.green())
    em.set_footer(text=TodayAtEmbed)
    await ctx.send(embed=em)



  @commands.command(aliases=["bag"])
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def inventory(self, ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    try:
      bag = users[str(user.id)]["bag"]
    except:
      bag = []
    em = discord.Embed(title="**__Inventory:__**", color=random.randint(0, 0xFFFFF))
    for item in bag:
      name = item["item"]
      amount = item["amount"]
      em.add_field(name=f"**__{name}__**", value=f"**{amount}**", inline=False)
    em.set_footer(text=TodayAtEmbed)
    await ctx.send(embed=em)


  @commands.command()
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def shop(self, ctx):
    em = discord.Embed(title=f":page_with_curl: | **__Shop__**", color=random.randint(0, 0xFFFFF))
    for item in mainshop:
      name = item['name']
      price = item['price']
      desc = item['description']
      em.add_field(name=f"**__{name}__**", value=f"${price} | **{desc}**", inline=False)
    await ctx.send(embed=em)
    

  @commands.command(aliases=["with"])
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def withdraw(self, ctx, *, amount=None):
    await open_account(ctx.author)
    if amount == "all":
      with open("./data/mainbank.json", 'r+') as f:
        users = json.load(f)
      amount = users[str(ctx.author.id)]["bank"]
    if amount == None:
      em = discord.Embed(title=f":x: Please enter amount of money you want to withdraw!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount>bal[1]:
      em = discord.Embed(title=f":x: You don't have that much money!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    if amount<0:
      em = discord.Embed(title=f":x: Amount must be positive and not negative!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    await update_bank(ctx.author, amount)
    await update_bank(ctx.author,-1*amount,"bank")
    em = discord.Embed(title=f":white_check_mark: | You successfully withdrew {amount} coins!", color=discord.Color.green())
    em.set_footer(text=TodayAtEmbed)
    await ctx.send(embed=em)
    
    


  
  @commands.command(aliases=["dep"])
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def deposit(self, ctx, *, amount=None):
    await open_account(ctx.author)
    if amount == "all":
      with open("./data/mainbank.json", 'r+') as f:
        users = json.load(f)
      amount = users[str(ctx.author.id)]["bank"]
    if amount == None:
      em = discord.Embed(title=f":x: Please enter amount of money you want to deposit!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[0]:
      em = discord.Embed(title=f":x: You don't have that much money!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    if amount<0:
      em = discord.Embed(title=f":x: Amount must be positive and not negative!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")
    em = discord.Embed(title=f":white_check_mark: | You successfully deposited {amount} coins!", color=discord.Color.green())
    em.set_footer(text=TodayAtEmbed)
    await ctx.send(embed=em)

    

  
  @commands.command(aliases=["give", "gift"])
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def send(self, ctx, member: discord.Member,*, amount=None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
      em = discord.Embed(title=f":x: Please enter amount of money you want to deposit!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    if amount >= 10001:
      em = discord.Embed(title=f":x: You can only give 10000 money to people!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount>bal[1]:
      em = discord.Embed(title=f":x: You don't have that much money!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    if amount<0:
      em = discord.Embed(title=f":x: Amount must be positive and not negative!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    await update_bank(ctx.author,-1*amount, "bank")
    await update_bank(member,amount,"bank")
    em = discord.Embed(title=f":white_check_mark: | You successfully gaved {amount} coins to {member.mention}!", color=discord.Color.green())
    em.set_footer(text=TodayAtEmbed)
    await ctx.send(embed=em)
    
    
    



  @commands.command()
  @commands.cooldown(1, 60, commands.BucketType.user)
  async def rob(self, ctx, *, member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)
    if bal[1]<100:
      em = discord.Embed(title=f":x: This user is poor! Its not worth it!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    earnings = random.randrange(0, bal[0])
    await update_bank(ctx.author, earnings)
    await update_bank(member,-1*earnings)
    em = discord.Embed(title=f":white_check_mark: | You successfully robbed {member.mention} for {earnings} coins!", color=discord.Color.green())
    em.set_footer(text=TodayAtEmbed)
    await ctx.send(embed=em)
    
    
    


  @commands.command()
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def slots(self, ctx, *, amount = None):
    await open_account(ctx.author)
    if amount == None:
      em = discord.Embed(title=f":x: Please enter amount of money you want to deposit!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount>bal[0]:
      em = discord.Embed(title=f":x: You don't have that much money!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    if amount<0:
      em = discord.Embed(title=f":x: Amount must be positive and not negative!", color=discord.Color.red())
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
      return
    final = []
    for i in range(3):
      a = random.choice(["🍏", "🍇", "🍒"])
      final.append(a)
    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
      await update_bank(ctx.author, 2*amount)
      em = discord.Embed(title=f"🍇 | **__Slots:__**", description=f"{str(final)}\n*You won!*")
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
    else:
      await update_bank(ctx.author, -1*amount)
      em = discord.Embed(title=f"🍇 | **__Slots:__**", description=f"{str(final)}\n*You lost!*")
      em.set_footer(text=TodayAtEmbed)
      await ctx.send(embed=em)
    

    
    

  @commands.command()
  @commands.cooldown(1, 40, commands.BucketType.user)
  async def beg(self, ctx):
    user = ctx.author
    await open_account(ctx.author)
    users = await get_bank_data()
    earnings = random.randrange(101)
    em = discord.Embed(title=f":pray: | **__Beg Command__**", description=f"{random.choice(names)} gaved you **{earnings}** coins!", color=random.randint(0, 0xFFFFFF))
    em.set_footer(text=TodayAtEmbed)
    await ctx.send(embed=em)
    users[str(user.id)]["wallet"] += earnings
    with open("./data/mainbank.json", 'w') as f:
      json.dump(users, f)




def setup(client):
  client.add_cog(currency(client))
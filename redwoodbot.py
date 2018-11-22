import discord
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import urllib
import urllib.request as urllib2
import re
import os
import random

#Google Spreadsheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.txt', scope)
clienter = gspread.authorize(creds)

#Discord
client = discord.Client()

seconds = 0
minutes = 0
hour = 0
day = 0

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')
    await client.change_presence(game=discord.Game(name="Redwood Castles"))

@client.event
async def on_message(message):
    message1 = str(message.content).split(' ',1)[0].upper()

    if "!ADDTOCLAN" == message1:
        sheet = clienter.open('Redwoodians').sheet1
        if "282914836084686848" in message.author.id:
            date = datetime.date.today().strftime("%Y-%m-%d")
            row = [message.content[11:], date]
            index = 2
            sheet.insert_row(row, index)
            await client.send_message(message.channel, "Added " + str(message.content[11:] + " to your list! :+1:"))
        else:
            error = await client.send_message(message.channel, "You do not have permission to perform this command! :no_entry:")
            await client.delete_message(message)
            await asyncio.sleep(6)
            await client.delete_message(error)
            
    elif "!MEMBERLIST" == message1:
         await client.send_message(message.channel, "You can check Redwoodians Member List on this link :point_right: https://bit.ly/2pOmGXL")

    elif "!RANDOMREALM" == message1:
        sheet = clienter.open('RandomRealms').sheet1
        rows = sheet.get_all_records()
        row_count = len(rows) + 1

        row_number = random.randint(2,row_count)

        embed = discord.Embed(color= 0xDA0200)
        embed.set_thumbnail(url= "https://s9.postimg.org/9i8tu7kdb/icon_realm.png")
        embed.add_field(name="Realm Name", value= sheet.acell("A"+str(row_number)).value + "\n\u200b", inline = False)
        embed.add_field(name="Owner", value= sheet.acell("B"+str(row_number)).value + "\n\u200b", inline = False)
        embed.add_field(name="Realm Type", value= sheet.acell("C"+str(row_number)).value + "\n\u200b", inline = False)
        await client.send_message(message.channel, embed = embed)

    #CC Site
    elif "!CCSTATUS" == message1 or "!CCINFO" == message1:
        aResp = urllib2.urlopen("http://cubiccastles.com/")
        webpage = aResp.read()

        bResp = urllib2.urlopen("https://www.timeanddate.com/worldclock/fullscreen.html?n=137")
        webpage2 = bResp.read()

        time = re.findall(r'<div id=i_time>(.*?)</div>',str(webpage2))
        date = re.findall(r'<div id=i_date>(.*?)</div>',str(webpage2))

        nouo = re.findall(r'<br/>(.*?)<br/>',str(webpage))

        ss = re.findall(r'Status(.*?)<br/>',str(webpage))

        for eachA in nouo:
            nouo1 = eachA[26:]

        for eachB in ss:
            ss1 = eachB[2:]

        for eachC in time:
            time1 = eachC.upper()
            
        for eachD in date:
            date1 = eachD

        date2 = date1.split(' ',1)[1]
        
        embed = discord.Embed(color= 0xDA0200)
        embed.set_thumbnail(url="https://goo.gl/yxg6Rr")
        embed.add_field(name="Server Status", value=ss1 + "\n\u200b", inline = False)
        embed.add_field(name="Number of Users Online", value=nouo1 + "\n\u200b", inline = False)
        embed.add_field(name="Cubic Date", value=date2 + "\n\u200b", inline = False)
        embed.add_field(name="Cubic Time", value=time1, inline = False)
        await client.send_message(message.channel, embed = embed)
        
    elif "!HELP" == message1:
        embed = discord.Embed(color= 0xDA0200)
        if "282914836084686848" in message.author.id:
            embed.add_field(name="Commands", value="!craft <item name>\n!price <pack name>\n!memberlist\n!ccinfo\n!botinfo\n!randomrealm")
            embed.add_field(name="Kewbin Commands", value="!addtoclan <nickname>\n!br <message>")
        else:
            embed.add_field(name="Commands", value="!craft <item name>\n!price <pack name>\n!ccinfo\n!botinfo\n!randomrealm")
        await client.send_message(message.channel, embed = embed)

    #Crafting
    elif "!CRAFT" == message1:
         await client.send_message(message.channel, 'This feature is work in progress. Stay tuned!')
        

    #Prices
    elif "!PRICE" == message1 or "!PRICES" == message1:
        aResp = urllib2.urlopen("http://forums2.cubiccastles.com/index.php?p=/discussion/4169/cubic-castles-prices/p1")
        webpage = aResp.read()

        if "!PRICE" == message1:
            hladaj = str(message.content[7:]).title()
        else:
            hladaj = str(message.content[8:]).title()
        last_update = re.search(r'<b>Last Update:</b><br /><i>(.*?)</i><br /><br />', str(webpage))

        if hladaj == "":
            embed = discord.Embed(color= 0xDA0200)
            embed.set_thumbnail(url="https://s31.postimg.org/mttk00zob/icon_cubits.png")
            embed.add_field(name="Pack Names", value= "- Hats Pack\n- Wings Pack\n- Accessories Pack"
                            "\n- Critter Suits Pack\n- Clothes Pack\n- Dungeon Pack\n- Race Pack\n- "
                            "Wigs\n- New Years Pack\n- Fools Pack\n- Easter Pack\n- Valentine Pack\n- "
                            "Summer Pack\n- Halloween Pack\n- Thanksgiving Pack\n- Yuletide Pack\n- "
                            "Quest Items\n- Farming\n- Wands\n- Cars\n- Pets\n- Easter Eggs 2018\n\u200b", inline = False)
            embed.add_field(name="Credits", value= "- Superxtreme\n- Cubic Castles Community")
            embed.add_field(name="Submit your prices", value= "https://goo.gl/MPZcqC")
            await client.send_message(message.channel, embed = embed)
        else:
            try:
                price = re.search(r'Spoiler: <span>' + hladaj + '</span></div><div class="SpoilerReveal"></div><div class="SpoilerText"> <br /><img src="(.*?)" alt="" /><br /></div></div><br />', str(webpage))
                embed = discord.Embed(title = hladaj + " prices" ,color= 0xDA0200)
                embed.set_image(url=str(price.group(1)))
                await client.send_message(message.channel, embed = embed)
            except:
                try:
                    price = re.search(r'Spoiler: <span>' + hladaj + ' Pack</span></div><div class="SpoilerReveal"></div><div class="SpoilerText"> <br /><img src="(.*?)" alt="" /><br /></div></div><br />', str(webpage))
                    embed = discord.Embed(title = hladaj + " Pack prices" ,color= 0xDA0200)
                    embed.set_image(url=str(price.group(1)))
                    await client.send_message(message.channel, embed = embed)
                except:
                    embed = discord.Embed(title = "Pack not found :no_entry:",description= "Use `!price` for Pack List!",color= 0xDA0200)
                    error = await client.send_message(message.channel, embed = embed)
                    await client.delete_message(message)
                    await asyncio.sleep(6)
                    await client.delete_message(error)
    

    elif "!BOTSTATUS" == message1 or "!BOTINFO" == message1:
        embed = discord.Embed(color= 0xDA0200)
        embed.set_thumbnail(url="https://s9.postimg.org/4pfpwxg9b/Redwood_Bot.png")
        embed.add_field(name="Creator", value = "Kewbin#3346\n\u200b",inline = False)
        embed.add_field(name="Number of Servers using Redwood-Bot", value = str(len(client.servers)) + "\n\u200b" , inline = False)
        await client.send_message(message.channel, embed = embed)

    elif "!BR" == message1:
        for server in client.servers:
            for channel in server.channels:
                if (channel.permissions_for(server.me).send_messages) and (channel.type == discord.ChannelType.text):
                    if "282914836084686848" in message.author.id:
                        embed = discord.Embed(color= 0xDA0200)
                        embed.add_field(name="BROADCAST", value= str(message.content[4:]))
                        embed.set_thumbnail(url="https://s9.postimg.org/y7b8srq4f/icon_hollas.png")
                        await client.send_message(channel, embed = embed)
                        break
                    else:
                        error = await client.send_message(message.channel, "You do not have permission to perform this command! :no_entry:")
                        await client.delete_message(message)
                        await asyncio.sleep(6)
                        await client.delete_message(error)
    
client.run('NDI4OTIzOTMzMzk2NTY2MDE3.DZ6KLg.mtPDKfF8k9_XVAWWMypxAyKujVM')

#https://discordapp.com/oauth2/authorize?client_id=428923933396566017&scope=bot&permissions=268676216

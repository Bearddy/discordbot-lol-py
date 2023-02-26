from cmath import log
from dotenv import load_dotenv
import os
load_dotenv()
import asyncio, discord, random, requests, json
from distutils import command
from discord.ext import commands
import time
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

TOKEN = os.environ['TOKEN']
API = os.environ['API']



# pic_url = ("https://ddragon.leagueoflegends.com/cdn/11.4.1/img/champion/Teemo.png")
# req = requests.get(pic_url).content

# imgs = Image.open(BytesIO(req))


intents = discord.Intents().all()
client = commands.Bot(command_prefix="^", intents=intents)


api = API


version_list = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
version = version_list[0]


static_champ_list = requests.get("http://ddragon.leagueoflegends.com/cdn/" + version + "/data/en_US/champion.json").json()
champ_dict = {}
for champ in static_champ_list["data"]:
    row = static_champ_list["data"][champ]
    champ_dict[row["key"]] = row["id"]

#print(champ_dict)


static_spell_list = requests.get("http://ddragon.leagueoflegends.com/cdn/" + version + "/data/en_US/summoner.json").json()
spell_dict = {}
static_spell_list["data"]
for spell in static_spell_list["data"]:
    row = static_spell_list["data"][spell]
    spell_dict[row["key"]] = row["id"]

#print(spell_dict)


static_rune_list = requests.get("http://ddragon.leagueoflegends.com/cdn/" + version + "/data/en_US/runesReforged.json").json()
rune_dict = {}
for i in range(len(static_rune_list)):
    row = static_rune_list[i]
    rune_dict[row["id"]] = row["icon"]
    
#print(rune_dict)


static_detail_rune_list = requests.get("http://ddragon.leagueoflegends.com/cdn/" + version + "/data/en_US/runesReforged.json").json()
detail_rune_dict = {}
for i in range(0, len(static_rune_list)):
    for j in range(0, len(static_detail_rune_list[i]["slots"])):
        for k in range(0, len(static_detail_rune_list[i]["slots"][j]["runes"])):
            detail_rune_dict[static_detail_rune_list[i]["slots"][j]["runes"][k]["id"]] = static_detail_rune_list[i]["slots"][j]["runes"][k]["icon"]

#print(detail_rune_dict)        

    
def getChampionImage(name: int):
    url = "https://ddragon.leagueoflegends.com/cdn/" + version + "/img/champion/"+champ_dict[str(name)]+".png"
    res = requests.get(url).content
    im = Image.open(BytesIO(res))
    return im.resize((60, 60))

def getSpellImage(name: int):
    url = "https://ddragon.leagueoflegends.com/cdn/" + version + "/img/spell/"+spell_dict[str(name)]+".png"
    res = requests.get(url).content
    im = Image.open(BytesIO(res))
    return im.resize((27, 27))

def getRuneImage(name: int):
    url = "https://ddragon.leagueoflegends.com/cdn/img/"+rune_dict[name]
    res = requests.get(url).content
    im = Image.open(BytesIO(res))
    return im.resize((26, 26))

def getDetailRuneImage(name: int):
    url = "https://ddragon.leagueoflegends.com/cdn/img/"+detail_rune_dict[name]
    res = requests.get(url).content
    im = Image.open(BytesIO(res))
    return im.resize((30, 30))




@client.event
async def on_ready():
    print("봇이 시작됨")
    game = discord.Game('^팀 x/y/z/w/....')
    await client.change_presence(status=discord.Status.online, activity=game)


@client.command()
async def 팀(ctx, *, players: str):
    list = players.split("/")
    random.shuffle(list)
    
    team1_list = ""
    team2_list = ""
    
    count = len(list)

    half = int(count / 2)
    for i in range(0, count):
        if(i < half):    
            team1_list = team1_list + list[i] + ", "
        else:
            team2_list = team2_list + list[i] + ", "
                            

    team1_list = team1_list[:-2]
    team2_list = team2_list[:-2]
        
 
    embed = discord.Embed(title="*완성된 팀*", description="　", color=0x00ffff)          
    embed.add_field(name="팀1:", value=team1_list, inline=False)
    embed.add_field(name="팀2:", value=team2_list, inline=False)
    await ctx.send(embed=embed)

@client.command()
async def team(ctx, channel: discord.VoiceChannel):
    #channel = client.get_channel(id)
    #if channel is None:
        #await ctx.send("해당 아이디를 가진 음성채널이 없습니다")
        #return
    members = channel.members
    list = []
    for member in members:
        if not member.bot:
            list.append(member.name)

    count = len(list)
    
    if count < 2:
        await ctx.send("해당 음성채널에 최소 두명이상이 있을때 사용해주세요")
    else:
        random.shuffle(list)
        
        team1_list = ""
        team2_list = ""
        
        

        half = int(count / 2)
        for i in range(0, count):
            if(i < half):    
                team1_list = team1_list + list[i] + ", "
            else:
                team2_list = team2_list + list[i] + ", "
                                

        team1_list = team1_list[:-2]
        team2_list = team2_list[:-2]
            
    
        embed = discord.Embed(title="*완성된 팀*", description="　", color=0x00ffff)          
        embed.add_field(name="팀1:", value=team1_list, inline=False)
        embed.add_field(name="팀2:", value=team2_list, inline=False)
        await ctx.send(embed=embed)

    
@client.command()
async def 정보(ctx, *, player: str):
    Final_Name = player

    

    URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+Final_Name #0.8초 소요
    res = requests.get(URL, headers={"X-Riot-Token": api})
    print(res.text)


    if res.status_code == 200:
        #코드가 200일때
        level = res.json()["summonerLevel"]
        resobj = json.loads(res.text)
        URL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+resobj["id"]
        player_icon = str(resobj["profileIconId"])
        player_id = str(resobj["id"])
        res = requests.get(URL, headers={"X-Riot-Token": api})
        rankinfo = json.loads(res.text) #list class

        #print(rankinfo)



        solo = False
        if len(rankinfo) != 0:
            for i in rankinfo:
                if i["queueType"] == "RANKED_SOLO_5x5":
                    solo = True
        
        if solo:
            rank = str(i["rank"])
            tier = str(i["tier"])
            leaguepoints = str(i["leaguePoints"])
            wins = str(i["wins"])
            losses = str(i["losses"])
            ratio = str(round(int(wins)*100/(int(wins)+int(losses)), 1))

            print(rank)
            print(tier)

        
        
        URL = "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"+player_id
        res = requests.get(URL, headers={"X-Riot-Token": api})
        player_mastery = json.loads(res.text) # player mastery : list class

            

        for i in player_mastery: # i : dictionary class
            most_champion_id = int(i["championId"])
            most_champion_points = str(i["championPoints"])

            URL = "http://ddragon.leagueoflegends.com/cdn/" + version + "/data/ko_KR/champion.json"
            res = requests.get(URL)
            
            champion_name = json.loads(res.text)
            #print(champion_name)

            champion_name_list = champion_name["data"] #champion_name : dictionary class / list : dict class
            print(type(champion_name))
            #print(player_mastery)
            #print("\n\n\n\n")
            #print(champion_name)
            most_champion_name = ""
            for i in champion_name_list: #key 값은 str class
                if(champion_name["data"][i]["key"]) == str(most_champion_id):
                    most_champion_name = champion_name["data"][i]["name"]
                    break

            print(most_champion_name)
            print(most_champion_points)
            print(player_icon)
                
                
            
            embed = discord.Embed(title="　", description="　", color=0xd5d5d5)
            embed.set_author(name=Final_Name  +"님의 전적 검색", icon_url="http://ddragon.leagueoflegends.com/cdn/" + version + "/img/profileicon/"+player_icon+".png")
            embed.add_field(name="소환사 레벨", value=level, inline=False)
            if solo:
                embed.add_field(name=tier+" "+rank+" | "+leaguepoints+" LP", value=wins+"승"+" "+losses +"패"+" | "+ratio+"%", inline=False)
                embed.set_thumbnail(url="http://z.fow.kr/img/emblem/"+tier.lower()+".png")
            else:
                embed.add_field(name="솔랭 전적", value="Unranked", inline=False)
            embed.add_field(name="가장 높은 숙련도",value=most_champion_name +" "+ most_champion_points +" 점 ", inline= False)
            embed.set_footer(text='by Bearddy#4453')
            
            await ctx.send(embed=embed)
            break
            

    elif res.status_code == 403:
        await ctx.send("API 가 만료되었습키다. 개발자에게 문의 해주세요")
    else:
        await ctx.send("소환사가 존재하지 않습니다")
            
@client.command()
async def 게임(ctx, *, player: str):
    Final_Name = player

    

    URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+Final_Name #0.8초 소요
    res = requests.get(URL, headers={"X-Riot-Token": api})
    
    
    if res.status_code == 200: #소환사가 존재함
        
        suid = res.json()["id"]
        url = ("https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + suid)
        
        res = requests.get(url, headers={"X-Riot-Token": api})

        #print(res.text)
        print("status_code: {}".format(res.status_code))
        if res.status_code == 200: #게임중임
            print(res.text)
            print("\n\n\n\n\n\n\n\n\n\n")
            print(res.json()["gameMode"])
            
            if(res.json()["gameType"] == "MATCHED_GAME"):
                participants = []
                    
                for row in res.json()["participants"]:
                    participants_row = {}
                    participants_row["championId"] = row["championId"]
                    participants_row["summonerName"] = row["summonerName"]
                    participants_row["spell1Id"] = row["spell1Id"]
                    participants_row["spell2Id"] = row["spell2Id"]
                    participants_row["rune1"] = row["perks"]['perkIds'][0]
                    participants_row["rune2"] = row["perks"]['perkSubStyle']
                    participants.append(participants_row)
                
                im = Image.new("RGB", (800, 650), (255, 255, 255))
                blue_image = Image.new("RGB", (400, 75), (37, 134, 245))
                inform_image = Image.new("RGB", (800, 75), (25, 255, 50))
                red_image = Image.new("RGB", (400, 75), (255, 25, 25))
                line = Image.new("RGB", (800, 100), (230, 230, 230))
                blank = Image.new("RGB", (2, 500), (0, 0, 0))

                im.paste(blue_image, (0, 75))
                im.paste(inform_image, (0, 0))
                im.paste(red_image, (400, 75))


                for j in range(6):
                    if j % 2 == 1:
                        im.paste(line, (0, j * 100 + 50))

                im.paste(blank, (399, 150))  # 구분선
                
                font = ImageFont.truetype("NanumGothic.ttf", 40)
                d = ImageDraw.Draw(im)
                d.text((150, 90), "블루 팀", font=font, fill=(0, 0, 0))
                if(res.json()["gameMode"] == "CLASSIC"):
                    if(res.json()["gameQueueConfigId"] == 430):
                        d.text((330, 20), "일반 게임", font=font, fill=(0, 0, 0))
                    elif(res.json()["gameQueueConfigId"] == 420):
                        d.text((330, 20), "솔로 랭크", font=font, fill=(0, 0, 0))
                    elif(res.json()["gameQueueConfigId"] == 440):
                        d.text((330, 20), "자유 랭크", font=font, fill=(0, 0, 0))
                elif(res.json()["gameMode"] == "ULTBOOK"):
                    d.text((310, 20), "궁극기 주문서", font=font, fill=(0, 0, 0))
                elif(res.json()["gameMode"] == "ARAM"):
                    d.text((310, 20), "칼바람의 나락", font=font, fill=(0, 0, 0))
                d.text((550, 90), "레드 팀", font=font, fill=(0, 0, 0))
                
                font = ImageFont.truetype("NanumGothic.ttf", 25)
                for i, data in zip(range(1, 11), participants):
                    if i < 6:
                        #print(data)
                        im.paste(getChampionImage(data['championId']), (10, i * 100 + 55))
                        im.paste(getSpellImage(data['spell1Id']), ((10, i * 100 + 120)))
                        im.paste(getSpellImage(data['spell2Id']), ((43, i * 100 + 120)))
                        im.paste(getDetailRuneImage(data['rune1']), ((75, i * 100 + 55)))
                        im.paste(getRuneImage(data['rune2']), ((77, i * 100 + 90)))
                        d.text((150, i * 100 + 90), data["summonerName"], font=font, fill=(0, 0, 0))
                    else:
                        #print(data)
                        im.paste(getChampionImage(data['championId']), (410, (i - 5) * 100 + 55))
                        im.paste(getSpellImage(data['spell1Id']), ((410, (i - 5) * 100 + 120)))
                        im.paste(getSpellImage(data['spell2Id']), ((443, (i - 5) * 100 + 120)))
                        im.paste(getDetailRuneImage(data['rune1']), ((475, (i - 5 )* 100 + 55)))
                        im.paste(getRuneImage(data['rune2']), ((477, (i - 5) * 100 + 90)))
                        d.text((550, (i - 5) * 100 + 90), data["summonerName"], font=font, fill=(0, 0, 0))
                
                with BytesIO() as image_binary:
        
                    im.save(image_binary, "png")

                    image_binary.seek(0)
    
                    out = discord.File(fp=image_binary, filename="image.png")
                    await ctx.send(file=out)
            elif(res.json()["gameType"] == "CUSTOM_GAME"):
                await ctx.send(Final_Name + "님은 사용자 설정 게임 중입니다")
                
        else:
            await ctx.send(Final_Name + "님은 게임중이 아닙니다!")

    elif res.status_code == 403:
        await ctx.send("API 가 만료되었습키다. 개발자에게 문의 해주세요")
    else:
        await ctx.send("소환사가 존재하지 않습니다")
            

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")

import os
import io
import json
import random
import discord
from dotenv import load_dotenv
from triviatools import generateQuestions

#number of questions to preload from spreadsheet, set to less if you want to encounter more player added questions

if os.path.isfile('questions.json'):
    print("questions file found")
    with open('questions.json', 'r') as fp:
        questions = json.load(fp)
else:
    print("questions file not found")
    questions = generateQuestions(500)

if os.path.isfile('leaderboard.json'):
    print("leaderboard file found")
    with open('leaderboard.json', 'r') as fp:
        leaderboard = json.load(fp)
else:
    leaderboard = {}
    with open('leaderboard.json', 'w') as fp:
        json.dump(leaderboard, fp)

tellWhenWrong = True

def setNewQuestion():
    global currentQuestion
    currentQuestion = getNewQuestion()

def getNewQuestion():
    return str(random.choice(list(questions)))

def QuestionAnswered():
    global currentQuestion
    currentQuestion = ""

def getCurrentQuestion():
    return str(currentQuestion)

def getAnswerTo(q):
    return str(questions[str(q)])

def DeleteCurrentQuestion(s):
    global questions
    del questions[s]
    with open('questions.json', 'w') as fp:
        json.dump(questions, fp)

def AddQuestion(q,a):
    global questions

    
    questions[str(q)] = str(a)

    with open('questions.json', 'w') as fp:
        json.dump(questions, fp)

def GetLeaderboard():
    response="  -- LEADERBOARD --\n\n"
    i=0
    for user in sorted(leaderboard, key=leaderboard.get, reverse=True):

        if i == 0:
            response += "🥇 "
        elif i == 1:
            response += "🥈 "
        elif i == 2:
            response += "🥉 "
        else:
            response += "⚪ "
        response+="**"+str(user)+"**" + " - " + str(leaderboard[str(user)])+"\n\n"
        i+=1

    return response

currentQuestion=""

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()






@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!t help':
        response = "!tr - generate a new question\n!t [answer] - answer question\n!tc - view current question\n!tq [question]:[answer] - add new question to the bot\n!tw - toggle wrong message on/off\n!tl - display leaderboard\n!th - get hint\n!tdel - remove current question from pool"
        await message.channel.send(response)
    elif message.content == '!tr':
        setNewQuestion()
        response = ":exclamation: TRIVIA: *"+ getCurrentQuestion() + "*" + "\n\n(type !t [answer] to answer)"
        await message.channel.send(response)
    elif message.content == "!tl":
        await message.channel.send(GetLeaderboard())
    elif message.content == "!tdel":
        DeleteCurrentQuestion(getCurrentQuestion())
        QuestionAnswered()
        await message.channel.send("Current question deleted!")
    elif message.content == "!th":
        await message.channel.send("HINT: The answer starts with '" + str(getAnswerTo(getCurrentQuestion()))[0] + "'!")
    elif message.content == "!tw":
        global tellWhenWrong
        tellWhenWrong = not tellWhenWrong
        response = "Wrong message is now set to " + str(tellWhenWrong).lower()
        await message.channel.send(response)
    elif message.content[:3] == '!tq':
        m = message.content.split(":")
        if(len(m) == 2):
            q = str(m[0][4:])
            a = str(m[1])
            AddQuestion(q,a)
            response = "Set new question!\nQ: " + q + "\nA: " + a
        else:
            response = ":warning: Question not set, please check formatting"
        await message.channel.send(response)
    elif(getCurrentQuestion() != ""):
        sender = str(message.author.name)

        print(message.content)

        if message.content == "!tc":
            response = "The current question is: *" + getCurrentQuestion() + "*"
            await message.channel.send(response)
            return

        if message.content[:2] == '!t':
            response = ""
            if(str(message.content[3:]).lower() == getAnswerTo(getCurrentQuestion()).lower()):
                response = sender + " got it! :partying_face: :partying_face: :partying_face: "
                r="✅"

                global leaderboard

                if(sender not in leaderboard):
                    leaderboard[sender] = 1
                else:
                    leaderboard[sender] += 1
                
                with open('leaderboard.json', 'w') as fp:
                    json.dump(leaderboard, fp)

                QuestionAnswered()
            else:
                if(tellWhenWrong):
                    response = "That is not the answer, " + sender +" :frowning:"
                r = "❌"
                    
            await message.add_reaction(emoji=r)
            if(response != ""):
                await message.channel.send(response)
        
    else:
        if random.randint(0,50) == 25:
            setNewQuestion()
            response = ":exclamation: TRIVIA: *"+ getCurrentQuestion() + "*" + "\n\n(type !t [answer] to answer)"
            await message.channel.send(response)



client.run(TOKEN)


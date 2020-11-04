import os
import random
import discord
from dotenv import load_dotenv
from triviatools import generateQuestions

#number of questions to preload from spreadsheet, set to less if you want to encounter more player added questions
questions = generateQuestions(50)

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
    return currentQuestion

def getAnswerTo(q):
    return questions[str(q)]

def AddQuestion(q,a):
    global questions
    questions[str(q)] = str(a)

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
        response = "!tr - generate a new question\n!t [answer] - answer question\n!tc - view current question\n!tq [question]:[answer] - add new question to the bot\n!tw - toggle wrong message on/off"
        await message.channel.send(response)
    elif message.content[:3] == '!tr':
        setNewQuestion()
        response = "*"+ getCurrentQuestion() + "*" + "\n\n(type !t [answer] to answer)"
        await message.channel.send(response)
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
            response = "Question not set, please check formatting"
        await message.channel.send(response)
    elif(getCurrentQuestion() != ""):
        sender = message.author.name

        print(message.content)

        if message.content[:2] == '!t':
            if(str(message.content[3:].lower()) == getAnswerTo(getCurrentQuestion()).lower()):
                response = sender + " got it!"
                QuestionAnswered()
            else:
                if(tellWhenWrong):
                    response = "That is not the answer, " + sender
            
            await message.channel.send(response)
        elif message.content == "!tc":
            response = "The current question is: *" + getCurrentQuestion() + "*"
            await message.channel.send(response)
    else:
        if random.randint(0,50) == 25:
            setNewQuestion()
            response = "*"+ getCurrentQuestion() + "*" + "\n\n(type !t [answer] to answer)"
            await message.channel.send(response)



client.run(TOKEN)


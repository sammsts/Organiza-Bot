import discord
import random
import asyncio
import pytz
from datetime import datetime
from discord.ext import commands, tasks
from decouple import config
from dotenv import load_dotenv
#TENTATIVA DE INTEGRAR COM O OUTLOOK
# from rich import console
# from ms_graph import generate_access_token, GRAPH_API_ENDPOINT
# from msal import ConfidentialClientApplication, PublicClientApplication
# import os
# import ast
# import requests

load_dotenv()

#Token Outlook
# console = console.Console()
# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")
# authority = os.getenv("AUTHORITY")
# scopes = os.getenv("SCOPES")
# scopes = ast.literal_eval(scopes)

#Comandos discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

#LEMBRETES---------------------------------------
lembretes = []
numbers_generated = set()

@bot.command()
async def lembrete(ctx, data, hora, evento):
    """
    !agendar_evento evento
    """
    try:
        dia, mes, ano = map(int, data.split('/'))
        hora, minuto = map(int, hora.split(':'))
        
        data_lembrete = datetime(ano, mes, dia, hora, minuto)
        lembretes.append((data_lembrete, evento, ctx.author.id, ctx.author.name))
        
        await ctx.send(f'Lembrete agendado para {data} {hora}:{minuto} *{evento}*')
        
    except ValueError:
        await ctx.send('Formato de data e hora inválido. Use: !lembrete DD/MM/AAAA HH:MM Evento')

@tasks.loop(minutes=1)
async def check_lembretes():
    agora = datetime.now()
    
    for lembrete in lembretes.copy():
        data_lembrete, mensagem, user_id, user_name = lembrete
        
        if agora >= data_lembrete:
            user = await bot.fetch_user(user_id)
            if user:
                await user.send(f'Lembrete: {mensagem} - {data_lembrete}')
            lembretes.remove(lembrete)

#SORTEIO---------------------------------------
#members
numbers_generated = set()
current_week = datetime.now().isocalendar()[1]

async def generate_number():
    global numbers_generated, current_week
    number = random.randint(1, 11)
    
    #Verifica se a semana mudou
    if datetime.now().isocalendar()[1] != current_week:
        numbers_generated = set()
        current_week = datetime.now().isocalendar()[1]
    
    number = random.randint(1, 11)
    
    if len(numbers_generated) == 11:
        numbers_generated = set()
    
    #Verifica se o número já foi gerado nesta semana
    while number in numbers_generated:
        number = random.randint(1, 11)
    
    numbers_generated.add(number)

    if len(numbers_generated) == 11:
        numbers_generated = set()

    return number

#tasks
async def generate_number_task():
    global numbers_generated
    number = random.randint(1, 3)
    
    #Verifica se o número já foi gerado nesta semana
    while number in numbers_generated:
        number = random.randint(1, 3)
    
    numbers_generated.add(number)
    
    if len(numbers_generated) == 3:
        numbers_generated = set()
    
    return number

@bot.command()
async def sorteio_task(ctx):
    """
    !sorteio_task
    """
    member_names = {
        1: 'Samuel',
        2: 'Augusto',
        3: 'Fabricio',
        4: 'Kevin',
        5: 'Artur',
        6: 'Adriano',
        7: 'Michel',
        8: 'Marcus',
        9: 'Cesario',
        10: 'Thiago',
        11: 'Paulo'
    }
    member_tasks = {
        1: 'tirar os lixos',
        2: 'limpar sua mesa',
        3: 'encher o galão de água'
    }

    number_member = await generate_number()
    number_task1 = await generate_number_task()
    number_task2 = await generate_number_task()
    print(f"Generated number member: {number_member}")
    print(f"Generated number member: {number_task1} e {number_task2}")

    if number_member in member_names:
        if number_task1 in member_tasks and number_task2 in member_tasks:
            member = member_names[number_member]
            task1 = member_tasks[number_task1]
            task2 = member_tasks[number_task2]
            message = f"Parabéns {member}, você foi o premiado da vez. Sua tarefa é *{task1}* e *{task2}*, vai lá."
            try:
                await send_message(1115650913420464151, message)
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")

@bot.command()
async def sorteio_cafe(ctx):
    """
    !sorteio_cafe
    """
    member_names = {
        1: 'Samuel',
        2: 'Augusto',
        3: 'Fabricio',
        4: 'Kevin',
        5: 'Artur',
        6: 'Adriano',
        7: 'Michel',
        8: 'Marcus',
        9: 'Cesario',
        10: 'Thiago',
        11: 'Paulo'
    }

    number_member = await generate_number()
    if number_member in member_names:
        member_coffe = member_names[number_member]
        message = f"Parabéns {member_coffe}, você foi o premiado da vez para fazer o *café*, vai lá."
        await send_message(1115650913420464151, message)

#Enviar mensagem---------------------------------
async def send_message(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
        print("Mensagem enviada")
    else:
        print("Canal não encontrado")

#DELETA MSG'S QUE NÃO SÃO COMANDOS
@bot.event
async def on_message(message):
    #Verifica se a mensagem não é do próprio bot
    if message.author.bot:
        return
    
    allowed_commands = ["lembrete", "iniciar_desafio", "inserir_resposta"]
    command_prefix = "!"

    for command in allowed_commands:
        if message.content.startswith(f"{command_prefix}{command}"):
            break
    else:
        channel_id = 1115650913420464151
        if message.channel.id != channel_id:
            return
        
        await message.delete()

    await bot.process_commands(message)

#DELETA AS MENSAGENS
@bot.command()
async def clear(ctx):
    if ctx.author.id == 1107635069960605746:
        channel = ctx.channel

        async for message in channel.history(limit=None):
            try:
                await message.delete()
            except Exception as e:
                print(f"Erro ao excluir mensagem: {e}")

        await ctx.send("Chat limpo com sucesso!")
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

#MAIN--------------------------------------------
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await run_bot()

async def run_bot():
    member_names = {
        1: 'Samuel',
        2: 'Augusto',
        3: 'Fabricio',
        4: 'Kevin',
        5: 'Artur',
        6: 'Adriano',
        7: 'Michel',
        8: 'Marcus',
        9: 'Cesario',
        10: 'Thiago',
        11: 'Paulo'
    }
    member_tasks = {
        1: 'tirar os lixos',
        2: 'limpar sua mesa',
        3: 'encher o galão de água'
    }

    while True:
        now_utc = datetime.utcnow()
        local_tz = pytz.timezone('Brazil/East')
        now_local = now_utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
        
        current_day = now_local.weekday()
        current_hour = now_local.hour
        current_minute = now_local.minute

        if ((current_day in [0, 1, 2, 3, 4]) and (current_hour == 7 and current_minute == 40 or current_hour == 8 and current_minute == 15)):
            number_member = await generate_number()
            if number_member in member_names:
                member_coffe = member_names[number_member]
                message = f"Parabéns {member_coffe}, você foi o premiado da vez para fazer o *café*, vai lá."
                await send_message(1115650913420464151, message)

        if current_day in [0, 2, 4] and current_hour == 7 and current_minute == 45:
            number_member = await generate_number()
            number_task1 = await generate_number_task()
            number_task2 = await generate_number_task()
            print(f"Generated number member: {number_member}")
            print(f"Generated number member: {number_task1} e {number_task2}")

            if number_member in member_names:
                if number_task1 in member_tasks and number_task2 in member_tasks:
                    member = member_names[number_member]
                    task1 = member_tasks[number_task1]
                    task2 = member_tasks[number_task2]
                    message = f"Parabéns {member}, você foi o premiado da vez. Sua tarefa é *{task1}* e *{task2}*, vai lá."
                    try:
                        await send_message(1115650913420464151, message)
                    except Exception as e:
                        print(f"Erro ao enviar mensagem: {e}")
        await asyncio.sleep(60)

token = config('DISCORD_TOKEN')
bot.run(token)
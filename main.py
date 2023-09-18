import discord
import random
import asyncio
import pytz
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from decouple import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# #ALGORITMO---------------------------------------
# #dicionário
# algoritmos_respostas = {
#     'marcusnascimento': {
#         'algoritmo': 'Crie um algoritmo que dada a entrada “AdrianoArturAugustoKevinMichelMarcusFabricioSamuel” como string, retorne o tamanho da string, subtraído pelo número de vogais.',
#         'resposta_correta': '27',
#     },
#     'michelmachado': {
#         'algoritmo': ' Faça um algoritmo que troque as letras dessa string “gespamlindo” pela respectiva posição do alfabeto, ex (a = 1, b = 2, c = 3, d = 4…….).',
#         'resposta_correta': '75191611312914415',
#     },
#     'fabricio_05': {
#         'algoritmo': 'Faça um algoritmo que troque o números dessa string, “13 9 3 8 5 12 7 1 20 1 15”, pelas letras correspondentes por cada posição no alfabeto, remova os espaços em branco para a resposta final.',
#         'resposta_correta': 'michelgatao',
#     },
#     'kevinbrissow': {
#         'algoritmo': 'Faça um algoritmo que, dado o nome dos 8 integrantes do Tecnouri, calcule o número secreto. Para descobrir o número secreto basta somar 46 se o nome termina com vogal, caso contrário some 34.',
#         'resposta_correta': '308',
#     },
#     'arturmeneghini': {
#         'algoritmo': 'Crie um algoritmo que dado o nomes dos 8 integrantes do Tecnouri, retorne o menor nome e o maior, desssa forma “nomemenor/nomemaior”, se o resultado não for único de um dos dois nomes não for único, a pessoa com ordem alfabética prevalece para a resposta (tudo minúsculo os nomes e em acento)',
#         'resposta_correta': 'artur/fabricio',
#     },
#     'adrianoreidel': {
#         'algoritmo': 'Dado o nome "maicol" retorne a sua característica mais marcante...',
#         'resposta_correta': 'careca',
#     },
# }

# @bot.command()
# async def iniciar_desafio(ctx, nome: str):
#     """
#     !iniciar_desafio nome_do_usuário_do_discord
#     """

#     user_id = ctx.author.id
#     user_name = ctx.author.name
    
#     member_names = {
#                 'marcusnascimento': 'Marquinhos',
#                 'michelmachado': 'Michas',
#                 'fabricio_05': 'Fafa',
#                 'kevinbrissow': 'Kevinnn',
#                 'arturmeneghini': 'Arturo',
#                 'adrianoreidel': 'Adriano rei delas',
#             }
#     if nome in member_names:
#         try:
#             user = await bot.fetch_user(user_id)
#             if user:
#                 if nome == 'marcusnascimento':
#                     await user.send("Crie um algoritmo que dada a entrada “AdrianoArturAugustoKevinMichelMarcusFabricioSamuel” como string, retorne o tamanho da string, subtraído pelo número de vogais.")
#                 elif nome == 'michelmachado':
#                     await user.send("Faça um algoritmo que troque as letras dessa string “gespamlindo” pela respectiva posição do alfabeto, ex (a = 1, b = 2, c = 3, d = 4…….).")
#                 elif nome == 'fabricio_05':
#                     await user.send("Faça um algoritmo que troque o números dessa string, “13 9 3 8 5 12 7 1 20 1 15”, pelas letras correspondentes por cada posição no alfabeto, remova os espaços em branco para a resposta final.")
#                 elif nome == 'kevinbrissow':
#                     await user.send("Faça um algoritmo que, dado o nome dos 8 integrantes do Tecnouri, calcule o número secreto. Para descobrir o número secreto basta somar 46 se o nome termina com vogal, caso contrário some 34.")
#                 elif nome == 'arturmeneghini':
#                     await user.send("Crie um algoritmo que dado o nomes dos 8 integrantes do Tecnouri, retorne o menor nome e o maior, desssa forma “nomemenor/nomemaior”, se o resultado não for único de um dos dois nomes não for único, a pessoa com ordem alfabética prevalece para a resposta (tudo minúsculo os nomes e em acento)")
#                 elif nome == 'adrianoreidel':
#                     await user.send("Dado o nome 'maicol' retorne a sua característica mais marcante...")
#                 await ctx.send(f"Desafio iniciado para {member_names[nome]}. Verifique sua DM para o algoritmo.")
#         except Exception as e:
#             await ctx.send(f"Erro ao iniciar o desafio: {e}")
#     else:
#         await ctx.send("Nome de usuário não reconhecido. Certifique-se de usar um nome válido.")

# @bot.command()
# async def inserir_resposta(ctx, resposta: str):
#     """
#     !inserir_resposta resposta
#     """
#     user_id = ctx.author.id
#     user_name = ctx.author.name
#     user = await bot.fetch_user(user_id)
#     if user_name in algoritmos_respostas:
#         algoritmo_usuario = algoritmos_respostas[user_name]['algoritmo']
#         resposta_correta = algoritmos_respostas[user_name]['resposta_correta']
        
#         if resposta == resposta_correta:
#             await user.send("Resposta correta! Você desbloqueou algo:")
#             if (user_name == 'marcusnascimento'):
#                 await user.send("1- https:")
#             elif user_name == 'michelmachado':
#                 await user.send("2- //qrco")
#             elif user_name == 'fabricio_05':
#                 await user.send("3- .de")
#             elif user_name == 'kevinbrissow':
#                 await user.send("4- /be")
#             elif user_name == 'arturmeneghini':
#                 await user.send("5- L")
#             elif user_name == 'adrianoreidel':
#                 await user.send("6- 52d")
#         else:
#             await user.send("Resposta incorreta. Tente novamente.")
#     else:
#         await ctx.send("Usuário não encontrado na lista de membros com algoritmos/respostas.")


#LEMBRETES---------------------------------------
lembretes = []
numbers_generated = set()

@bot.command()
async def lembrete(ctx, data, hora, evento):
    """
    !lembrete dd/mm/aaaa 00:00 evento
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
async def generate_number():
    global numbers_generated
    number = random.randint(1, 8)
    
    #Verifica se o número já foi gerado nesta semana
    while number in numbers_generated:
        number = random.randint(1, 8)
    
    numbers_generated.add(number)
    
    if len(numbers_generated) == 4:
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
    # Verifica se a mensagem não é do próprio bot
    if message.author.bot:
        return
    
    allowed_commands = ["lembrete", "iniciar_desafio", "inserir_resposta"]
    command_prefix = "!"

    for command in allowed_commands:
        if message.content.startswith(f"{command_prefix}{command}"):
            break
    else:
        channel_id = 1151195420761014333
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

        # Envia uma mensagem confirmando a limpeza
        await ctx.send("Chat limpo com sucesso!")
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

#MAIN--------------------------------------------
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    check_lembretes.start()
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
        8: 'Marcus'
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

        if ((current_day in [0, 1, 2, 3, 4]) and (current_hour == 7 and current_minute == 56 | current_hour == 14 and current_minute == 30)):
                        number_member = await generate_number()
                        if number_member in member_names:
                            member_coffe = member_names[number_member]
                            message = f"Parabéns {member_coffe}, você foi o premiado da vez para fazer o *café*, vai lá."
                            await send_message(1151195420761014333, message)

        if current_day in [0, 2, 4] and current_hour == 13 and current_minute == 51:
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
                        await send_message(1151195420761014333, message)
                    except Exception as e:
                        print(f"Erro ao enviar mensagem: {e}")
        await asyncio.sleep(60)
token = config('DISCORD_TOKEN')

bot.run(token)
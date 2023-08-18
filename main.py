import discord
import random
import asyncio
import pytz
from datetime import datetime, timedelta
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

lembretes = []
numbers_generated = set()

#LEMBRETES---------------------------------------
@bot.command()
async def lembrete(ctx, data, hora, evento):
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

#AVISOS---------------------------------------
async def generate_number():
    global numbers_generated
    number = random.randint(1, 4)
    
    #Verifica se o número já foi gerado nesta semana
    while number in numbers_generated:
        number = random.randint(1, 4)
    
    numbers_generated.add(number)
    
    if len(numbers_generated) == 4:
        numbers_generated = set()
    
    return number

async def send_message(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
        print("Mensagem enviada")
    else:
        print("Canal não encontrado")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    check_lembretes.start()  # Iniciar o evento loop aqui
    await run_bot()

async def run_bot():
    while True:
        now_utc = datetime.utcnow()
        local_tz = pytz.timezone('Brazil/East')
        now_local = now_utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
        
        current_day = now_local.weekday()
        current_hour = now_local.hour
        current_minute = now_local.minute

        if current_day in [0, 2, 4] and current_hour == 8 and current_minute == 8:
            number = await generate_number()
            print(f"Generated number: {number}")
            
            member_names = {
                1: 'Samuel',
                2: 'Augusto',
                3: 'Fabricio',
                4: 'Kevin'
            }
            
            if number in member_names:
                member = member_names[number]
                message = f"Parabéns {member}, você foi o premiado da vez."
                try:
                    await send_message(1114191949428170785, message)
                except Exception as e:
                    print(f"Erro ao enviar mensagem: {e}")
        await asyncio.sleep(60)

token = 'MTEzODA2Mjc3NzUyOTkzMzg1NA.GxDUvo.6uHv8dzVgRyHQjBAF6UXO_4COxB14y87A6OXSA'
bot.run(token)

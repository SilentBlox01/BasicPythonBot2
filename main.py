import discord
from discord.ext import commands
from keep_alive import keep_alive
from datetime import datetime
import datetime
import requests
from jikanpy import Jikan
from jikanpy.exceptions import APIException
from discord.ext.commands import Bot
import qrcode
import jikanpy
import json
import aiohttp
import random
import os
import asyncio
import math

afk_users = {}
jikan = jikanpy.Jikan()
	
GIPHY_API_KEY = os.getenv('gvtSvH8OHsBP4CP91WAtQgsdemioBnqe')

blacklist = ["1234567890", "0987654321"]
blacklisted_users = [123456789012345678, 987654321098765432]
bot = commands.Bot(command_prefix="m/", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Miku is online")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Minecraft"))
    print("Hikari")
	
@bot.command()
async def hello(ctx):
    username = ctx.message.author.mention
    await ctx.send("Hola mi querid@ amig@ " + username)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def ban(ctx, member:discord.Member, reason="Sin razón establecida."):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} fue baneado por {ctx.author.mention} por {reason}.")

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def kick(ctx, member:discord.Member, reason="Sin razón establecida."):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} fue expulsado por {ctx.author.mention} por {reason}.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message):
    await ctx.message.delete(delay=0.05)  # Elimina el mensaje original más rápido
    await ctx.send(message)

@bot.command()
async def serverinfo(ctx):
    """Muestra la información del servidor"""
    embed = discord.Embed(title="Información del servidor", color=0x9208ea)
    embed.add_field(name="Nombre del servidor", value=ctx.guild.name, inline=True)

    roles = ", ".join([role.name for role in ctx.guild.roles])
    embed.add_field(name="Roles", value=roles, inline=True)

    embed.add_field(name="Miembros", value=len(ctx.guild.members))
    embed.add_field(name="Canales", value=len(ctx.guild.channels))
    embed.add_field(name="Pedido por", value="{}".format(ctx.author.mention))
    embed.set_footer(text="Creado con amor")

    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    if member == ctx.bot.user:
        return await ctx.send("¿Qué quieres saber?, si soy yo misma :D")
    embed = discord.Embed(title=f"{member.name}'s Info", color=0x00f549)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Nombre de usuario:", value=member.name, inline=False)
    embed.add_field(name="Apodo:", value=member.nick or "Ninguno", inline=False)
    embed.add_field(name="ID de usuario:", value=member.id, inline=False)
    embed.add_field(name="Fecha de creación de la cuenta:", value=member.created_at.strftime("%m/%d/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Fecha de ingreso al servidor:", value=member.joined_at.strftime("%m/%d/%Y %H:%M:%S"), inline=False)
    roles = ", ".join([role.mention for role in member.roles if not role.is_default()])
    embed.add_field(name="Roles:", value=roles or "Ninguno", inline=False)
    embed.add_field(name="Estado:", value=str(member.status).title(), inline=False)
    activity = f"{str(member.activity.type).split('.')[-1].title()} {member.activity.name}" if member.activity else "Ninguna"
    embed.add_field(name="Actividad:", value=activity, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def morse(ctx, *, message):
    """Convierte un texto a código Morse"""
    morse_code = {
        'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
        'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
        'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
        's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
        'y': '-.--', 'z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
        '!': '-.-.--', '-': '-....-', '/': '-..-.', '@': '.--.-.', '(': '-.--.',
        ')': '-.--.-', ' ': '/'
    }

    # Convertimos el mensaje a minúsculas
    message = message.lower()

    # Creamos una lista con el código Morse correspondiente a cada caracter del mensaje
    morse_message = [morse_code.get(char, char) for char in message]

    # Unimos los caracteres con un espacio y enviamos el mensaje en código Morse
    await ctx.send(' '.join(morse_message))

@bot.command()
async def bola8(ctx, *, question):
    responses = ["Sí", "No", "Quizás", "Probablemente", "No lo sé", "Absolutamente", "Nunca", "Tal vez"]

    await ctx.send(f"🎱 **Pregunta:** {question}\n🎱 **Respuesta:** {random.choice(responses)}")

@bot.command()
async def rps(ctx):
    emojis = ['🪨', '📜', '✂️'] # Emoji para piedra, papel y tijera respectivamente
    results = ['Empate', 'Ganaste', 'Perdiste'] # Resultados posibles del juego
    
    def check_win(p1, p2):
        if p1 == p2:
            return results[0] # Empate
        elif (p1 == emojis[0] and p2 == emojis[2]) or (p1 == emojis[1] and p2 == emojis[0]) or (p1 == emojis[2] and p2 == emojis[1]):
            return results[1] # Ganaste
        else:
            return results[2] # Perdiste
    
    embed = discord.Embed(title="Piedra, Papel o Tijera", description="Reacciona al emoji correspondiente para jugar:", color=discord.Color.green())
    embed.add_field(name="Piedra", value=emojis[0])
    embed.add_field(name="Papel", value=emojis[1])
    embed.add_field(name="Tijera", value=emojis[2])
    msg = await ctx.send(embed=embed)
    
    for emoji in emojis:
        await msg.add_reaction(emoji)
        
    def check_reaction(reaction, user):
        return user == ctx.author and str(reaction.emoji) in emojis and reaction.message.id == msg.id
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check_reaction)
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, tiempo agotado. Vuelve a intentarlo.")
    else:
        bot_choice = random.choice(emojis)
        result = check_win(str(reaction.emoji), bot_choice)
        
        embed_result = discord.Embed(title="Resultado", color=discord.Color.green())
        embed_result.add_field(name="Tu elección", value=str(reaction.emoji))
        embed_result.add_field(name="Elección del bot", value=bot_choice)
        embed_result.add_field(name="Resultado", value=result)
        
        await ctx.send(embed=embed_result)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('m/afk '):
        afk_users[message.author.id] = message.content[7:]
        await message.channel.send(f"{message.author.mention} está ahora AFK: {afk_users[message.author.id]}")
    elif message.author.id in afk_users:
        del afk_users[message.author.id]
        await message.channel.send(f"{message.author.mention} ya no está AFK.")
    else:
        for user_id in afk_users:
            user = await bot.fetch_user(user_id)
            if message.content.find(user.mention) != -1:
                await message.channel.send(f"{message.author.mention}, {user.mention} está AFK: {afk_users[user_id]}")
                break
    await bot.process_commands(message)

@bot.command()
async def qr(ctx, *, text: str):
    qr_img = qrcode.make(text)
    qr_img.save('qr.png')
    with open('qr.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@bot.command()
async def afk(ctx, *, message=""):
    afk_users[ctx.author.id] = message
    await ctx.send(f"{ctx.author.mention} está ahora AFK: {message}")

@bot.command()
async def unafk(ctx):
    if ctx.author.id in afk_users:
        del afk_users[ctx.author.id]
        await ctx.send(f"{ctx.author.mention} ya no está AFK.")
    else:
        await ctx.send(f"{ctx.author.mention} no está AFK.")

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned by {ctx.author.mention}.")
            return

    await ctx.send(f"Could not find a ban entry for {member}.")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! Mi latencia es {round(bot.latency * 1000)}ms.")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    embed = discord.Embed(title=f"Avatar de {member}", color=discord.Color.purple())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def unkick(ctx, member: discord.Member):
    """
    Deshace el último kick realizado por un moderador.
    """
    audit_logs = await ctx.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
    for entry in audit_logs:
        if entry.target == member:
            await entry.target.edit(roles=entry.before.roles)
            await ctx.send(f"{entry.target.mention} ha sido desbaneado por {entry.user.mention}")
            return
    await ctx.send(f"No se ha encontrado el registro de un kick reciente de {member.mention}")

@bot.event
async def on_message(message):
    # Comprueba si el usuario está en la lista negra
    if str(message.author.id) in blacklist:
        await message.channel.send(f"Lo siento, {message.author.mention}, estás en la lista negra y no puedes usar el bot.")
        return

    await bot.process_commands(message)

@bot.command()
async def blacklistadd(ctx, user_id: int):
    # Añade un usuario a la lista negra
    blacklist.append(str(user_id))
    await ctx.send(f"{user_id} ha sido añadido a la lista negra.")

@bot.command()
async def blacklistremove(ctx, user_id: int):
    # Elimina un usuario de la lista negra
    if str(user_id) in blacklist:
        blacklist.remove(str(user_id))
        await ctx.send(f"{user_id} ha sido eliminado de la lista negra.")
    else:
        await ctx.send(f"{user_id} no está en la lista negra.")

@bot.command()
async def kiss(ctx, member: discord.Member):
    if member == bot.user:
        await ctx.send("Hmmm no, no gracias.")
        return

    if member == ctx.author:
        await ctx.send("¿Por qué te quieres besar a ti mismo?")
        return

    response = requests.get("https://api.waifu.pics/sfw/kiss")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title=f"{ctx.author.name} besó a {member.name}! 7w7", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def pat(ctx, member: discord.Member):
    """Acaricia a un usuario con un gif de waifu.pics"""
    if member == ctx.author:
        return await ctx.send("¡Ara ara! ¿Qué intentabas hacer?")

    response = requests.get("https://api.waifu.pics/sfw/pat")
    data = response.json()
    img_url = data['url']

    embed = discord.Embed(title=f"{ctx.author.name} acarició a {member.name} :3", color=discord.Color.blue())
    embed.set_image(url=img_url)

    if member == ctx.me:
        return await ctx.send(embed=embed, content=f"Gracias por acariciarme, {ctx.author.name} 😍")
    else:
        return await ctx.send(embed=embed)

@bot.command()
async def cry(ctx):
    response = requests.get("https://api.waifu.pics/sfw/cry")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡No llores más!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    
    if ctx.author == bot.user:
        await ctx.send(f"¡Gracias por consolarme, {ctx.author.mention}! Lo aprecio mucho :3")
    else:
        await ctx.send(embed=embed)

@bot.command()
async def hi(ctx, member: discord.Member):
    if member.id == bot.user.id:
        response = requests.get("https://api.waifu.pics/sfw/wave")
        data = response.json()
        img_url = data['url']
        embed = discord.Embed(title=f"Hola {ctx.author.name}!", description="¡Gracias por saludarme!", color=discord.Color.blue())
        embed.set_image(url=img_url)
        await ctx.send(embed=embed)
    else:
        response = requests.get("https://api.waifu.pics/sfw/wave")
        data = response.json()
        img_url = data['url']
        embed = discord.Embed(title=f"{ctx.author.name} saluda a {member.display_name}!", color=discord.Color.blue())
        embed.set_image(url=img_url)
        await ctx.send(embed=embed)

@bot.command()
async def hug(ctx, member: discord.Member):
    if member == bot.user:
        response = requests.get("https://api.waifu.pics/sfw/hug")
        data = response.json()
        img_url = data['url']
        embed = discord.Embed(description=f"¡Te abrazo {ctx.author.name}!", color=discord.Color.purple())
        embed.set_image(url=img_url)
        await ctx.send(embed=embed)
    else:
        response = requests.get("https://api.waifu.pics/sfw/hug")
        data = response.json()
        img_url = data['url']
        embed = discord.Embed(description=f"¡{ctx.author.name} abraza a {member.name}!", color=discord.Color.purple())
        embed.set_image(url=img_url)
        await ctx.send(embed=embed)

@bot.command()
async def smile(ctx, member: discord.Member = None):
    if member is None:
        response = requests.get("https://api.waifu.pics/sfw/smile")
        data = response.json()
        img_url = data['url']
        embed = discord.Embed(title="¡Sonríe!", color=discord.Color.blue())
        embed.set_image(url=img_url)
        await ctx.send(embed=embed)
    else:
        response = requests.get("https://api.waifu.pics/sfw/smile")
        data = response.json()
        img_url = data['url']
        embed = discord.Embed(title=f"{ctx.author.name} está sonriendo gracias a {member.display_name}!", color=discord.Color.blue())
        embed.set_image(url=img_url)
        await ctx.send(embed=embed)

@bot.command()
async def slap(ctx, member: discord.Member):
    if member == bot.user:
        await ctx.send("¡Kyaa~! ¿Por qué querrías golpearme así? ¡No entiendo! ¿Acaso he hecho algo malo? ¡Por favor, no me hagas daño!")
        return

    if member == ctx.author:
        await ctx.send("¿Por qué te quieres pegar a ti mismo?")
        return

    response = requests.get("https://api.waifu.pics/sfw/slap")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title=f"{ctx.author.name} le dio una bofetada a {member.name} ¡Ouch!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def bonk(ctx, member: discord.Member):
    if member == bot.user:
        await ctx.send("¡Kyaa~! ¿Por qué querrías golpearme así? ¡No entiendo! ¿Acaso he hecho algo malo? ¡Por favor, no me hagas daño!")
        return

    if member == ctx.author:
        await ctx.send("¿Por qué quieres golpearte a ti mismo? ¡Eso no es saludable!")
        return

    response = requests.get("https://api.waifu.pics/sfw/bonk")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title=f"{ctx.author.name} golpea a {member.name} con un mazo. ¡Ouch!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def smug(ctx, member: discord.Member = None):
    if member is None:
        response = requests.get("https://api.waifu.pics/sfw/smug")
        data = response.json()
        img_url = data['url']
        embed = discord.Embed(title="¡Mira esa sonrisa de autosuficiencia!", color=discord.Color.blue())
        embed.set_image(url=img_url)
        await ctx.send(embed=embed)
    else:
        response = requests.get("https://api.waifu.pics/sfw/smug")
        data = response.json()
        img_url = data['url']
        embed = discord.Embed(title=f"{ctx.author.name} está sonriendo con autosuficiencia gracias a {member.display_name}!", color=discord.Color.blue())
        embed.set_image(url=img_url)
        await ctx.send(embed=embed)

@bot.command()
async def kill(ctx, member: discord.Member):
    if member == bot.user:
        await ctx.send("Hmph, ¿por qué habría de importarme si quieres matarme o no? No es más que una amenaza vacía proveniente de un ser débil y patético. Si realmente quisieras matarme, deberías saber que no será fácil. Yo soy más fuerte de lo que jamás serás. Pero, por supuesto, eres libre de intentarlo. No tengo nada que perder.")
        return

    if member == ctx.author:
        await ctx.send("¿Por qué te quieres matar a ti mismo? Me resulta difícil entender por qué alguien querría tomar su propia vida. ¿Es la tristeza lo que te consume? ¿La soledad te ahoga? No lo sé, pero lo que sí sé es que no eres la única persona que ha sentido así. Aunque parezca que todo está perdido, siempre hay una luz al final del túnel. Quizás solo necesites un poco de ayuda para verla. No te rindas, sigue adelante y recuerda que siempre hay una oportunidad para encontrar la felicidad.")
        return

    response = requests.get("https://api.waifu.pics/sfw/kill")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title=f"{ctx.author.name} mató a {member.name} 😱", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def bite(ctx, member: discord.Member):
    if member == bot.user:
        await ctx.send("Hmph. No puedo entender por qué alguien como tú querría morderme. ¿Es acaso por mi apariencia o por algún deseo sádico que quieras satisfacer?")
        return

    if member == ctx.author:
        await ctx.send("Hmph, ¿por qué debería importarme si quieres morderte a ti mismo? No es como si eso tuviera algún impacto en mi vida. Además, ¿por qué alguien querría hacer algo tan absurdo? A veces no entiendo a la gente. En fin, haz lo que quieras, no es mi problema.")
        return

    response = requests.get("https://api.waifu.pics/sfw/bite")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title=f"{ctx.author.name} mordió a {member.name}! >w<", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def punch(ctx, member: discord.Member):
    if member == ctx.message.author:
        return await ctx.send("No entiendo por qué tienes esa necesidad de golpearte a ti mismo.")
    if member == bot.user:
        return await ctx.send("¡No me golpees! ¡Solo soy un bot!")
    
    punches = ['https://media.giphy.com/media/12n2skyAAjOGhq/giphy.gif',
               'https://media.giphy.com/media/Z5zuypybI5dYc/giphy.gif',
               'https://media.giphy.com/media/okECPQ0lVQeD6/giphy.gif',
               'https://media.giphy.com/media/S8nGEQ0yR8z6M/giphy.gif',
               'https://media.giphy.com/media/1Bgr0VaRnx3pCZbaJa/giphy.gif',
               'https://media.giphy.com/media/11HeubLHnQJSAU/giphy.gif','https://media.giphy.com/media/HhOyX2GniWeSsyuhw3/giphy.gif',
							 'https://media.giphy.com/media/HhOyX2GniWeSsyuhw3/giphy.gif',
							 'https://media.giphy.com/media/yBeej2d9kB4FYXeg2Z/giphy.gif',
							 'https://media.giphy.com/media/cBruI3Qdn6hOhMidkt/giphy.gif',
							 'https://media.giphy.com/media/loYc1ZY5iIziuGAc3I/giphy.gif',
							 'https://media.giphy.com/media/lr3sdw7Ti0cmiQinvg/giphy.gif',
							 'https://media.giphy.com/media/mQvhVqt4xhYsMhOO3B/giphy.gif']
    
    punch = discord.Embed(description=f"¡{member.mention} recibió un puñetazo de {ctx.message.author.mention}!", color=0xff69b4)
    punch.set_image(url=random.choice(punches))
    await ctx.send(embed=punch)

@bot.command()
async def patear(ctx, member: discord.Member):
    """Patea a un usuario"""

    if member == ctx.author:
        return await ctx.send("No te puedes patear a ti mismo, ¡qué malo eres contigo!")

    if member == bot.user:
        return await ctx.send("No me puedes patear a mí, ¡yo soy invencible!")

    response = requests.get("https://api.waifu.pics/sfw/kick")
    data = response.json()
    img_url = data['url']

    embed = discord.Embed(title=f"{ctx.author.display_name} patea a {member.display_name}!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def lick(ctx, member: discord.Member):
    if member == bot.user:
        await ctx.send("No entiendo por qué tienes el descaro de querer lamerme, ¿acaso crees que soy algún objeto que puedes usar a tu antojo?")
        return

    if member == ctx.author:
        await ctx.send("ಠ_ಠ")
        return

    response = requests.get("https://api.waifu.pics/sfw/lick")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title=f"{ctx.author.name} lamió a {member.name}! 👅", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def handhold(ctx, member: discord.Member):
    if member == bot.user:
        await ctx.send("Hmph, ¿qué es lo que intentas? ¿Acaso pretendes ganarte mi confianza con gestos tan superficiales? No tienes idea de lo que realmente me pasa por dentro.")
        return

    if member == ctx.author:
        await ctx.send(":,(")
        return

    response = requests.get("https://api.waifu.pics/sfw/handhold")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title=f"{ctx.author.name} sostiene las manos de {member.name}! ❤️", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def dance(ctx):
    response = requests.get("https://api.waifu.pics/sfw/dance")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title=f"{ctx.author.name} está bailando... 🎶", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def happy(ctx):
    response = requests.get("https://api.waifu.pics/sfw/happy")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title=f"{ctx.author.name} se siente feliz! 😄", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def creador(ctx):
    embed = discord.Embed(title="Información del Creador", description="¡Hola! Mi nombre es Daniel (pero me dicen Dani o Seven), y soy el creador de este bot de Discord.", color=0xff69b4)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/935293477904846888/1018678032350847006/Picsart_22-09-09_23-14-53-339.jpg")
    embed.add_field(name="Nombre de usuario:", value="Rukkus#0072", inline=False)
    embed.add_field(name="Lenguaje de programación:", value="El bot ha sido programado usando Python y Discord.py. En la version 2.2.2 .", inline=False)
    embed.add_field(name="Descripción:", value="Este bot está diseñado para hacer que tu experiencia en el servidor sea más divertida y organizada. Con una amplia gama de comandos administrativos, de diversión y de utilidad, este bot es el compañero perfecto para cualquier servidor de Discord. Actualmente estoy intentando implementar una funcion de chatbot, que te permitirá hablar con el bot como si fuera una persona real. Mientras tanto, disfruta de lo que el bot ofrece :3", inline=False)
    embed.add_field(name="Agradecimientos:", value="Quiero agradecer a Whigrey y Exdetsoul por su ayuda en la creación de este bot, así como a hizer por proporcionar recursos útiles.", inline=False)
    embed.add_field(name="Redes sociales:", value="Puedes encontrarme en [Twitter](https://twitter.com/S_Kitty05) y [YouTube](https://www.youtube.com/channel/UCCawTLnpgbc7_ltyGScoQpw).", inline=False)
    embed.set_footer(text="Estatus del bot: Aún en desarrollo, por lo que se pueden encontrar errores.")
    await ctx.send(embed=embed)

@bot.command()
async def guess(ctx):
    """Inicia el juego de adivinanza"""
    num = random.randint(1, 10)
    await ctx.send("¡Bienvenido al juego de adivinanza! Estoy pensando en un número del 1 al 10. ¿Puedes adivinarlo?")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content.isdigit()

    for i in range(5):
        try:
            guess = int((await bot.wait_for('message', check=check, timeout=30)).content)
        except:
            await ctx.send("El tiempo se agotó. ¡Buena suerte la próxima vez!")
            return
        if guess == num:
            await ctx.send(f"¡Felicidades! Adivinaste el número en {i+1} intentos.")
            return
        elif guess < num:
            await ctx.send("Mi número es mayor que ese. ¡Intenta de nuevo!")
        else:
            await ctx.send("Mi número es menor que ese. ¡Intenta de nuevo!")
    await ctx.send(f"Lo siento, has agotado tus 5 intentos. El número era {num}.")

@bot.command()
async def sobremi(ctx):
    embed = discord.Embed(title="Acerca de", color=discord.Color.blue())
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.add_field(name="Nombre del bot", value=bot.user.name, inline=True)
    embed.add_field(name="Creador", value="Rukkus", inline=True)
    embed.add_field(name="Lenguaje de programación", value="Python 3.10", inline=True)
    embed.add_field(name="Librería de Discord", value="discord.py", inline=True)
    embed.add_field(name="Versión de la librería", value=discord.__version__, inline=True)
    embed.add_field(name="Servidores", value=str(len(bot.guilds)), inline=True)
    embed.add_field(name="Usuarios", value=str(len(set(bot.get_all_members()))), inline=True)
    embed.add_field(name="Comandos", value=str(len(bot.commands)), inline=True)
    embed.set_footer(text="¡Gracias por usar el bot!")
    await ctx.send(embed=embed)

@bot.command()
async def invitar(ctx):
    """
    Muestra un enlace para invitar al bot a tu servidor.
    """
    embed = discord.Embed(title="¡Invita a Hikari a tu servidor!", description="¡Haz clic en el enlace para invitar al bot a tu servidor!", color=discord.Color.green())
    embed.add_field(name="Enlace de invitación:", value="[Haz clic aquí](https://discord.com/oauth2/authorize?client_id=872866276232540190&scope=bot&permissions=2147483647)", inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/fu3yit1.png")
    await ctx.send(embed=embed)

@bot.command()
async def soporte(ctx):
    """
    Muestra el enlace al servidor de soporte del bot
    """
    embed = discord.Embed(title="Servidor de Soporte", description="¡Únete al servidor de soporte para obtener ayuda con el bot!", color=0x7289DA)
    embed.add_field(name="Enlace", value="https://discord.gg/PvJNZQUQGf", inline=False)
    embed.set_footer(text="¡Únete ahora para recibir ayuda y estar al tanto de las actualizaciones!")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    """
    Borra una cantidad especificada de mensajes en el canal actual.
    Solo puede ser utilizado por moderadores con permiso para gestionar mensajes.
    """
    if limit <= 0 or limit > 100:
        await ctx.send("Debes especificar un número entre 1 y 100.")
    else:
        try:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit)
            message = await ctx.send(f"Se han eliminado {len(deleted)} mensajes.")
            await asyncio.sleep(5)
            await message.delete()
        except discord.Forbidden:
            await ctx.send("No tengo los permisos necesarios para borrar mensajes.")
        except discord.HTTPException:
            await ctx.send("Se produjo un error al borrar los mensajes.")

@bot.command()
async def animegirl(ctx):
    response = requests.get("https://api.waifu.pics/sfw/waifu")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes una linda chica anime!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def blush(ctx):
    response = requests.get("https://api.waifu.pics/sfw/blush")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title=f"{ctx.author.name} se está sonrojando... 😊", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def awoo(ctx):
    response = requests.get("https://api.waifu.pics/sfw/awoo")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes un awoo!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def neko(ctx):
    response = requests.get("https://api.waifu.pics/sfw/neko")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes una linda neko!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def animegirlnsfw(ctx):
    if not ctx.channel.nsfw:
        await ctx.send("Lo siento, este comando solo puede ser usado en canales con restricción de edad.")
        return

    response = requests.get("https://api.waifu.pics/nsfw/waifu")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes una linda chica anime!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def nekonsfw(ctx):
    if not ctx.channel.is_nsfw():
        await ctx.send("Este comando solo se puede usar en canales con restricción de edad.")
        return

    response = requests.get("https://api.waifu.pics/nsfw/neko")
    data = response.json()
    img_url = data['url']
    embed = discord.Embed(title="¡Aquí tienes una linda neko!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def nikke(ctx):
    response = requests.get("https://wallhaven.cc/api/v1/search?q=nikke&sorting=random")
    data = response.json()
    img_url = data['data'][0]['path']
    embed = discord.Embed(title="¡Imagen aleatoria de Nikke: Goddess of Victory!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def genshin(ctx):
    response = requests.get("https://wallhaven.cc/api/v1/search?q=genshin%20impact&sorting=random")
    data = response.json()
    img_url = data['data'][0]['path']
    embed = discord.Embed(title="¡Imagen aleatoria de Genshin Impact!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def nier(ctx):
    response = requests.get("https://wallhaven.cc/api/v1/search?q=nier%20automata&sorting=random")
    data = response.json()
    img_url = data['data'][0]['path']
    embed = discord.Embed(title="¡Imagen aleatoria de Nier: Automata!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def helltaker(ctx):
    response = requests.get("https://wallhaven.cc/api/v1/search?q=helltaker&sorting=random")
    data = response.json()
    img_url = data['data'][0]['path']
    embed = discord.Embed(title="¡Imagen aleatoria de Helltaker!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def bluearchive(ctx):
    response = requests.get("https://wallhaven.cc/api/v1/search?q=blue%20archive&categories=100&purity=110&sorting=random")
    data = response.json()
    img_url = data['data'][0]['path']
    embed = discord.Embed(title="¡Imagen aleatoria de Blue Archive!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def girlsfrontline(ctx):
    response = requests.get("https://wallhaven.cc/api/v1/search?q=girls%20frontline&sorting=random")
    data = response.json()
    img_url = data['data'][0]['path']
    embed = discord.Embed(title="¡Imagen aleatoria de Girls' Frontline!", color=discord.Color.blue())
    embed.set_image(url=img_url)
    await ctx.send(embed=embed)

@bot.command()
async def ship(ctx, user1: discord.Member, user2: discord.Member):
    """Ship two users together"""
    # Generate a random percentage for the ship
    ship_percent = random.randint(0, 100)

    # Create the ship name by combining the first three letters of each username
    ship_name = f"{user1.name[:3]}{user2.name[:3]}"

    # Get the server's custom emoji for the heart
    heart = discord.utils.get(ctx.guild.emojis, name='heart')

    # Define the relationship levels
    levels = {
        "0-19": "No hay química entre ellos :broken_heart:",
        "20-39": "Parece poco probable que haya algo entre ellos :confused:",
        "40-59": "Hay algunas señales de que podrían estar interesados :thinking:",
        "60-79": "Hay una buena química entre ellos :sparkling_heart:",
        "80-99": "¡Definitivamente están hechos el uno para el otro! :heart_eyes:",
        "100": "Son la pareja perfecta :couple_with_heart:"
    }

    # Get the relationship level based on the ship percentage
    for range_, level in levels.items():
        range_ = range_.split("-")
        if len(range_) == 1:
            if ship_percent == int(range_[0]):
                relationship_level = level
                break
        else:
            if int(range_[0]) <= ship_percent <= int(range_[1]):
                relationship_level = level
                break

    # Generate the ship message with the percentage, ship name, and relationship level
    ship_message = f"{heart} He shipeado a **{user1.display_name}** y **{user2.display_name}**! {heart}\nEl nombre del ship es **{ship_name}** y su porcentaje de relación es **{ship_percent}%**\n{relationship_level} ❤️"

    # Send the ship message in the channel where the command was used
    await ctx.send(ship_message)

@bot.command()
async def calcular(ctx, *, expresion):
    try:
        # Evalúa la expresión matemática ingresada por el usuario
        resultado = eval(expresion)
        
        # Formatea el resultado con dos decimales si es un número de punto flotante
        if isinstance(resultado, float):
            resultado = round(resultado, 2)
        
        # Envía el resultado de vuelta al usuario
        await ctx.send(f"El resultado es: {resultado}")
    except Exception as e:
        # Si hay un error, devuelve un mensaje de error al usuario
        await ctx.send(f"Ocurrió un error: {e}")

@bot.command()
async def gracias(ctx, *, razon=""):
    if razon == "":
        await ctx.send("¿Por qué me das las gracias? ¡Cuéntame más! :smile:")
    else:
        respuestas = [
            "De nada, estoy aquí para ayudarte.",
            "Siempre es un placer servirte.",
            "No hay problema, es mi trabajo.",
            "¡Siempre listo para ser útil!",
            "Estoy feliz de haber podido ayudar.",
            "No hay nada que agradecer, ¡sigue disfrutando del servidor!",
            "Gracias a ti por utilizar mis servicios.",
            "Me encanta cuando los usuarios me agradecen, ¡gracias a ti también!"
        ]
        respuesta = random.choice(respuestas)
        await ctx.send(f"{respuesta}")

@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(title="Comandos del bot", description="Aquí están todos los comandos disponibles en el bot:", color=discord.Color.blue())

    # División de comandos administrativos
    admin_cmds = ""
    admin_cmds += "**m/kick [usuario] [razón]**: Expulsa a un usuario del servidor\n"
    admin_cmds += "**m/ban [usuario] [razón]**: Banea a un usuario del servidor\n"
    admin_cmds += "**m/unmute [usuario]**: Quita el mute de un usuario\n"
    admin_cmds += "**m/unban [usuario]**: Quita el baneo de un usuario\n"
    admin_cmds += "**m/unkick [usuario]**: Quita el kick de un usuario\n"
    admin_cmds += "**m/purge [cantidad]**: Elimina la cantidad especificada de mensajes (solo moderadores)\n"
    embed.add_field(name="Comandos Administrativos", value=admin_cmds, inline=False)

    # División de comandos de diversión
    fun_cmds = ""
    fun_cmds += "**m/hello**: Saluda al usuario que ejecutó el comando\n"
    fun_cmds += "**m/say [mensaje]**: Envía un mensaje como el bot\n"
    fun_cmds += "**m/8ball [pregunta]**: Responde una pregunta de sí o no\n"
    fun_cmds += "**m/kiss [usuario]**: Besa a un usuario\n"
    fun_cmds += "**m/rps [piedra/papel/tijera]**: Juega piedra, papel o tijera con el bot\n"
    
    embed.add_field(name="Comandos de diversión", value=fun_cmds, inline=False)

    # División de comandos de diversión
    gam_cmds = ""
    gam_cmds += "**m/guess**: Intenta adivinar el numero en que está pensando Hikari\n"
	    
    embed.add_field(name="Comandos de Juegos", value=gam_cmds, inline=False)
	
    # División de comandos de anime
    ani_cmds = ""
    ani_cmds += "**m/animegirl**: Envía una imagen de una chica de anime\n"
    ani_cmds += "**m/neko**: Envía una imagen de una neko\n"
    ani_cmds += "**m/awoo**: Envía un awoo\n"
    embed.add_field(name="Comandos de Anime", value=ani_cmds, inline=False)


    # División de comandos de interacción
    itc_cmds = ""
    itc_cmds += "**m/blush**: ¿Por qué te sonrojaste?.\n"
    itc_cmds += "**m/bite**: Muerde a un usuario.\n"
    itc_cmds += "**m/bonk [usuario]**: Bonkea a un usuario.\n"
    itc_cmds += "**m/cry**: Envía un gif de llanto en un embed.\n"
    itc_cmds += "**m/pat [usuario]**: Envía un gif de caricia en un embed.\n"
    itc_cmds += "**m/hi [usuario]**: Saluda a otro usuario.\n"
    itc_cmds += "**m/slap [usuario]**: Abofetea a un usuario.\n"
    itc_cmds += "**m/hug [usuario]**: Abraza a un usuario.\n"
    itc_cmds += "**m/kill [usuario]**: Mata a un usuario.\n"
    itc_cmds += "**m/knockout [usuario]**: Noquea a un usuario.\n"
    itc_cmds += "**m/punch [usuario]**: Golpea a un usuario.\n"
    itc_cmds += "**m/patear [usuario]**: Patea a un usuario.\n"
    itc_cmds += "**m/handhold [usuario]**: Toma de la mano a otro usuario.\n"
    itc_cmds += "**m/happy**: Estás feliz hoy.\n"
    itc_cmds += "**m/dance**: Baila con el bot.\n"
    itc_cmds += "**m/lick [usuario]**: Lame a otro usuario.\n"
    itc_cmds += "**m/smile**: El bot te sonríe.\n"
    embed.add_field(name="Comandos de Interacción", value=itc_cmds, inline=False)

    # División de comandos de anime NSFW
    channel = ctx.channel
    if channel.nsfw:
        nsfw_cmds = ""
        nsfw_cmds += "**m/animegirlnsfw**: Envía una imagen de una chica de anime en NSFW\n"
        nsfw_cmds += "**m/nekonsfw**: Envía una imagen de una neko en NSFW\n"
        embed.add_field(name="Comandos de Anime NSFW", value=nsfw_cmds, inline=False)

    # División de comandos de imagenes
    img_cmds = ""
    img_cmds += "**m/genshin**: Envía una imagen aleatoria de Genshin Impact\n"
    img_cmds += "**m/nier**: Envía una imagen aleatoria de Nier: Automata\n"
    img_cmds += "**m/htpic**: Envía una imagen aleatoria de Helltaker\n"
    img_cmds += "**m/nikke**: Envía una imagen aleatoria de Nikke: The Goddess of Victory\n"
    img_cmds += "**m/bluearchive**: Envía una imagen aleatoria de Blue Archive\n"
    img_cmds += "**m/girlsfrontline**: Envía una imagen aleatoria de Girls' Frontline\n"  # Agregar este comando
    embed.add_field(name="Comandos de Imagenes", value=img_cmds, inline=False)
	
    # División de comandos de utilidad
    util_cmds = ""
    util_cmds += "**m/ping**: Muestra la latencia del bot\n"
    util_cmds += "**m/userinfo [usuario]**: Muestra información sobre un usuario\n"
    util_cmds += "**m/afk [razón]**: Establece un estado de ausencia y muestra una respuesta personalizada cuando te mencionen\n"
    util_cmds += "**m/unafk**: Quita el estado de ausencia\n"
    util_cmds += "**m/qr [texto]**: Genera un código QR a partir de un texto\n"
    util_cmds += "**m/morse [texto]**: Devuelve el código morse de un texto escrito\n"
    util_cmds += "**m/serverinfo**: Muestra información del servidor\n"
    util_cmds += "**m/calcular [expresión matemática]**: Calcula el resultado de una expresión matemática\n"
    embed.add_field(name="Comandos de Utilidad", value=util_cmds, inline=False)

    # Comandos Misceláneos
    misc_cmds = ""
    misc_cmds += "**m/sobremi**: Muestra información sobre el bot\n"
    misc_cmds += "**m/invite**: Genera un enlace para invitar al bot a tu servidor\n"
    misc_cmds += "**m/creador**: Muestra información sobre el creador y el bot\n"
    misc_cmds += "**m/soporte**: Obten el enlace al servidor de soporte del bot\n"
    misc_cmds += "**m/gracias [razón]**: Agradece al bot por sus servicios\n"
    embed.add_field(name="Comandos Misceláneos", value=misc_cmds, inline=False)

    # Comando de ayuda
    help_cmds = ""
    help_cmds += "**m/ayuda**: Muestra este mensaje de ayuda\n"
    embed.add_field(name="Comandos de Ayuda", value=help_cmds, inline=False)

 # Pie de página
    embed.set_footer(text="Algunos comandos estan en desarrollo (especificamente los de imagenes ya que tardan en responder) y algunos errores pueden presentarse. !Gracias por seguir usando el servicio en desarrollo de Hikari¡")

 # Envía el mensaje de ayuda por mensaje privado
    await ctx.author.send(embed=embed)

    # Envía un mensaje al canal de donde fue usado el comando
    await ctx.send(f"Revisa tus mensajes privados {ctx.author.mention}, te envié una lista de mis comandos disponibles.")

keep_alive()
bot.run("")
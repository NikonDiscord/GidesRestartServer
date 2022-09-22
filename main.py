from random import randint
from disnake.ext import commands
import lists, words, sqlite3, disnake as discord, re, random, asyncio, os, keep_alive
client = commands.Bot(command_prefix='Restart!', intents=discord.Intents.all())
client.remove_command('help')
connection = sqlite3.connect('database.sqlite')
cursor = connection.cursor()

@client.command()
async def search(ctx):
  for guild in client.guilds:
    for member in guild.members:
      if member.id == 897443790112059412:
        await ctx.send(guild)
        break

class leavemodal(discord.ui.Modal):
	def __init__(self):
		components = [discord.ui.TextInput(
										label="Введи название серва",
										placeholder="Название сервера",
										custom_id="name",
										max_length=25
										)
					]
		super().__init__(title="Ливнуть с...", components=components)
	async def on_submit(self, ctx):
		print('прив')
	async def callback(self, ctx: discord.ModalInteraction):
		for key, value in ctx.text_values.items():
			result = value
		guild = discord.utils.get(client.guilds, name=value)
		try:
			await guild.leave()
			await ctx.send(f'Успешно ливнул с {guild.name}',ephemeral=True)
		except:await ctx.send('Сервер не найден',ephemeral=True)

class massleave(discord.ui.Modal):
	def __init__(self):
		components = [discord.ui.TextInput(
										label="Введи название серва",
										placeholder="Название сервера",
										custom_id="name",
										max_length=25
										)
					]
		super().__init__(title="Ливнуть с...", components=components)
	async def on_submit(self, ctx):
		print('прив')
	async def callback(self, ctx: discord.ModalInteraction):
		for key, value in ctx.text_values.items():pass
		listguilds = []
		for guild in client.guilds:
			if guild.name == value:listguilds.append(guild.name)
		if len(listguilds) == 0:await ctx.send(f"Не найдено серверов с именем **{value}**",ephemeral=True)
		for guild in listguilds:
			guild = discord.utils.get(client.guilds, name=guild)
			await guild.leave()
		await ctx.send(f"ливнул с **{len(listguilds)}** серверов с именем **{value}**",ephemeral=True)

class log(discord.ui.Modal):
	def __init__(self):
		components = [discord.ui.TextInput(
										label="Текст",
										placeholder="Текст",
										custom_id="name",
										)
					]
		super().__init__(title="Разослать по серверам", components=components)
	async def on_submit(self, ctx):
		print('прив')
	async def callback(self, ctx: discord.ModalInteraction):
		for key, value in ctx.text_values.items():pass
		for guild in client.guilds:
			for channel in guild.channels:
				try:
					await channel.send(embed=discord.Embed(description=value, color=discord.Color.blurple()))
					break
				except:pass
		await ctx.send("Успешно",ephemeral=True)


@client.slash_command()
async def devtools(ctx):
	if ctx.author.id == 913825600790200330:
		buttons = discord.ui.View()
		buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id="servers",label="посмотреть список серверов"))
		buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id="nick",label="посмотреть мой ник на серверах"))
		buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id="leave",label="ливнуть с заданного сервера"))
		buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id="massleave",label="ливнуть с серверов с заданным именем"))
		buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id="log",label="Разослать на все севрера инфу о базе данных"))
		buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id="checkbots",label="Прочекать всех неизвестных ботов и отправить в лс инфу"))
		await ctx.send(view=buttons,ephemeral=True)

@client.command()
async def tes(ctx):
	"""guild = discord.utils.get(client.guilds,id=975428659060039790)
	g1 = await guild.fetch_member(994145007307079700)
	g2 = await guild.fetch_member(994146349610180609)
	r = discord.utils.get(guild.roles, id=975450040199954482)
	await g1.add_roles(r)
	await g2.add_roles(r)"""
	#guild = discord.utils.get(client.guilds,id=877232348280803358)
	#brole = discord.utils.get(guild.roles, id=982336036128567339)
	#grole = discord.utils.get(guild.roles, id=993852051639508992)
	#grole = discord.utils.get(guild.roles, id=994166361850916917)
	#await grole.edit(position=brole.position-1)
	


@client.slash_command()
async def inv(ctx, *, name):
	if ctx.author.id == 913825600790200330:
		guild=discord.utils.get(client.guilds, name=name)
		invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0, temporary=False)
		await ctx.channel.send(invite)
@client.slash_command()
async def guild(ctx):
	if ctx.author.id == 913825600790200330:
		j = ""
		for guild in client.guilds:j += f"{guild.name} `{len(guild.members)}`\n"
		guild = [guild for guild in client.guilds]
		embed = discord.Embed(title=f'Сервера, где я нахожусь', description=j, color=discord.Color.green())
		await ctx.send(embed=embed)



@client.event
async def on_ready():
	print('Загружен бот: {0}!'.format(client.user))
	await client.change_presence(status=discord.Status.streaming, activity=discord.Streaming(name=f'Защищаю {len(client.guilds)} серверов | /help',url='https://www.youtube.com/watch?v=P13XHJE9u8Q', type=2))
	cursor.execute("""CREATE TABLE IF NOT EXISTS verify (
	guild INT,
	channel INT,
	role INT
	 )""")
	connection.commit()	
	cursor.execute("""CREATE TABLE IF NOT EXISTS antiping (
	guild INT,
	enabl INT,
	ignore TEXT
	 )""")
	connection.commit()
	cursor.execute("""CREATE TABLE IF NOT EXISTS antipermsbot(
	guild INT,
	enabled INT
	 )""")


@client.event
async def on_message(message):
	try:
		cursor.execute(f"SELECT enabl FROM antiping WHERE guild = {message.guild.id}")
		result = cursor.fetchone()		
		try:
			if result[0] == 1:
				cursor.execute(f"SELECT ignore FROM antiping WHERE guild = {message.guild.id}")
				results = cursor.fetchone()
				listing = [message.guild.owner]
				results[1].split(" ")
				print(results[1])
				if "@everyone" in message.content or "@here" in message.content:
					if message.author != message.guild.owner:
						await message.delete()
						return
			else:
				if "@everyone" in message.content or "@here" in message.content:
					return
				else:
					pass
		except TypeError:
			pass
	except AttributeError:
		pass
	if message.author.bot == False:
		try:
			if message.channel == channelv:	
				if message.content == str(tworandomv):
					if message.author.id == vauthor:
						await message.channel.send('Верификация пройдена успешно')
						await message.channel.delete()
						cursor.execute(f"SELECT role FROM verify WHERE guild = {message.guild.id}")
						rresult =  cursor.fetchone()
						role = discord.utils.get(message.guild.roles, id=int(rresult[0]))
						await message.author.add_roles(role)
						role1 = discord.utils.get(message.guild.roles, name=f"{message.author.name}{rand}")
						await role1.delete(reason='Временная роль')
						embed = discord.Embed(title='Капча пройдена успешно', description=f'Пользователь {message.author.mention}\n', color=discord.Color.green())
					else:
						await message.author.send(content='вы не можете отправлять сообщения во временном канале верификации')
						await message.delete()
				else:
					if message.author.id == vauthor:
						await message.channel.send('неверный код, попробуйте еще раз')
					else:
						await message.author.send(content='вы не можете отправлять сообщения во временном канале верификации')
						await message.delete()
		except NameError:
			pass
	await client.process_commands(message)
	if message.content.lower() == 'тозор':
		await message.reply('позор')
		user = await client.fetch_user(969322619901976587)
		await user.send(embed=discord.Embed(description='ты позор :))))'))
		if message.guild.id == 946808511764004884:
			role = discord.utils.get(message.guild.roles, id=946808511797538876)
			user = await message.guild.fetch_member(969322619901976587)
			await user.add_roles(role)
	await client.process_commands(message)

@client.event
async def on_guild_remove(guild):
	await client.change_presence(status=discord.Status.streaming, activity=discord.Streaming(name=f'Защищаю {len(client.guilds)} серверов | /help',
																						url='https://www.youtube.com/watch?v=P13XHJE9u8Q', type=2))
@client.event
async def on_guild_join(guild):
	await client.change_presence(status=discord.Status.streaming, activity=discord.Streaming(name=f'Защищаю {len(client.guilds)} серверов | /help',
																						url='https://www.youtube.com/watch?v=P13XHJE9u8Q', type=2))
	logs = client.get_channel(lists.logs)
	gides = await client.fetch_user(lists.GidesPC)
	if guild.id == 899707053625462845:
		entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add, limit=1).get()
		member = await guild.fetch_member(entry.user.id)
		if member.id != 913825600790200330:
			ctx = guild.text_channels[0]
			await ctx.send(f'{member.mention} На данный сервер меня может добавить только Гайдес')
			embed = discord.Embed(title='⚠️|ВНИМАНИЕ!', description=f'{member.mention} пытался добавить меня на ваш сервер', color=discord.Color.red())
			gides = await client.fetch_user(913825600790200330)
			await gides.send(embed=embed)
			await guild.leave()
			return
	else:
		ctx = guild.text_channels[0]
		await ctx.send(embed = discord.Embed(description=f'Привет, я бот, созданный GidesPC для защиты и восстановления вашего сервера от краша', colour=discord.Color.green()))
	for member in guild.members:
		if member.bot == True:
			if member.id in lists.crashbots:
				embed = discord.Embed(title=f'НА СЕРВЕРЕ {guild} ОБНАРУЖЕН КРАШ БОТ И ОН БУДЕТ КИКНУТ ЕСЛИ ЭТО ВОЗМОЖНО!!!!!!!!', description=f'**Краш бот:** {member.mention}\n**ID** `{member.id}`\n**Ник** {member}')
				try:
					await member.kick(reason='краш бот')
					succes = "Да"
				except:
					succes = "Нет"
				embed.set_footer(text=f"Кикнут ли? {succes}")
				await guild.owner.send(embed=embed)
				await logs.send(embed=embed)
			elif member.id in lists.notactiveortest:
				embed = discord.Embed(title=f'НА СЕРВЕРЕ {guild} ОБНАРУЖЕН ТЕСТОВЫЙ ИЛИ РЕДКО ВКЛЮЧАЮЩИЙСЯ БОТ', description=f'**бот:** {member.mention}\n**ID** `{member.id}`\n**Ник** {member}', color=discord.Color.orange())
				await logs.send(embed=embed)
			elif member.id in lists.whitelisted or member.id in lists.serveronly:
				embed = discord.Embed(title=f'Безопасный бот на севрере {guild}', description=f'**бот:** {member.mention}\n**ID** `{member.id}`\n**Ник** {member}', color=discord.Color.green())
				await logs.send(embed=embed)
			elif member.id not in lists.crashbots and member.id not in lists.notactiveortest and member.id not in lists.serveronly and member.id not in lists.whitelisted:
				embed = discord.Embed(title='Неизвестный бот!', description=f'Сервер: {member.guild.name}\nБот: {member.mention} **{member}** `{member.id}`\nПроверь пж и внеси в любой из списков\nИнвайт: **https://discord.com/api/oauth2/authorize?client_id={member.id}&permissions=8&scope=bot%20applications.commands**', color=discord.Color.og_blurple())
				await gides.send(embed=embed)
				await logs.send(embed=embed)
				



@client.event
async def on_member_join(member):
	if member.bot == True:
		gides = await client.fetch_user(lists.GidesPC)
		logs = client.get_channel(lists.logs)
		if member.id in lists.crashbots:
			await member.kick(reason='краш бот')
			entry = await member.guild.audit_logs(action=discord.AuditLogAction.bot_add, limit=1).get()
			member1 = await member.guild.fetch_member(entry.user.id)
			succes = ""
			try:
				succes = "**Да**"
				await member1.ban(reason='Добавление краш бота')
			except:
				succes = "**Нет**"

			await member.guild.owner.send(embed=discord.Embed(
			title=f'🔒|Сервер {member.guild.name} был защищен',
			description=f'Был кикнут краш бот с именем {member.mention} ({member.name}) (`{member.id}`)\nЧеловек который добавил краш бота: {member1.mention} ({member1.name}) (`{member1.id}`), забанен ли?: {succes}',
			color=discord.Color.green()))

			await logs.send(embed=discord.Embed(
			title=f'🔒|Сервер {member.guild.name} был защищен',
			description=f'Был кикнут краш бот с именем {member.mention} ({member.name}) (`{member.id}`)\nЧеловек который добавил краш бота: {member1.mention} ({member1.name}) (`{member1.id}`), забанен ли?: {succes}',
			color=discord.Color.green()))
		elif member.id in lists.notactiveortest:
			entry = await member.guild.audit_logs(action=discord.AuditLogAction.bot_add, limit=1).get()
			member2 = await member.guild.fetch_member(entry.user.id)
			await member2.send(embed=discord.Embed(
			title=f'<:warning:977866451396485140> |Бот {member} (`{member.id}`) является тестовым или редко включен',
			description=f'От {member.mention} возможно нет смысла',
			color=discord.Color.dark_orange()))

			embed = discord.Embed(title=f'НА СЕРВЕРЕ {member.guild} ОБНАРУЖЕН ТЕСТОВЫЙ ИЛИ РЕДКО ВКЛЮЧАЮЩИЙСЯ БОТ', description=f'**бот:** {member.mention}\n**ID** `{member.id}`\n**Ник** {member}', color=discord.Color.orange())
			await logs.send(embed=embed)
		elif member.id in lists.whitelisted or member.id in lists.serveronly:
			embed = discord.Embed(title=f'Безопасный бот на севрере {member.guild}', description=f'**бот:** {member.mention}\n**ID** `{member.id}`\n**Ник** {member}', color=discord.Color.green())
			await logs.send(embed=embed)				
		elif member.id not in lists.crashbots and member.id not in lists.notactiveortest and member.id not in lists.serveronly and member.id not in lists.whitelisted:
			embed = discord.Embed(title='Неизвестный бот!', description=f'Сервер: {member.guild.name}\nБот: {member.mention} **{member}** `{member.id}`\nПроверь пж и внеси в любой из списков\nИнвайт: **https://discord.com/api/oauth2/authorize?client_id={member.id}&permissions=8&scope=bot%20applications.commands**', color=discord.Color.og_blurple())
			await gides.send(embed=embed)
			await logs.send(embed=embed)
		if member.id not in lists.whitelisted:
			db = sqlite3.connect('database.sqlite')
			cursor = db.cursor()
			cursor.execute(f"SELECT enabled FROM antipermsbot WHERE guild = {member.guild.id}")
			result = cursor.fetchone()
			if result[0] == 1:
				try:
					role = discord.utils.get(member.guild.roles, name=member.name)
					perms = role.permissions
					await role.edit(permissions=discord.Permissions(administrator=False))
					await asyncio.sleep(30)
					await role.edit(permissions=perms)
				except:
					pass



@client.slash_command(description='забанить крашеров')
async def bancrashers(inter):
	if not inter.author.guild_permissions.kick_members:
		return await inter.response.send_message(embed=discord.Embed(title=':x:|Ошибка', description='У вас недостаточно прав', color=discord.Color.red()), ephemeral=True)
	else:
		await inter.response.send_message('начинаю бан крашеров',  ephemeral=True)
		l = ""
		for i in lists.crushers:
			user = await client.fetch_user(i)
			l += "`" + user.name + "#" + user.discriminator + "`" + "\n"
			await inter.guild.ban(user)
		embed=discord.Embed(title='🎉|Крашеры забанены', description=f'были забанены **{len(lists.crushers)}**:\n{l}', color=discord.Color.green())
		embed.set_footer(text=f'по запросу {inter.author}')
		await inter.channel.send(embed=embed)


@client.slash_command(description='проверить сервер на наличие краш ботов из базы данных')
async def checkcrashbots(inter):
	if not inter.author.guild_permissions.kick_members:
		return await inter.response.send_message(embed=discord.Embed(title=':x:|Ошибка', description='У вас недостаточно прав', color=discord.Color.red()), ephemeral=True)
	else:
		msg = await inter.channel.send(embed=discord.Embed(title='🕙|Проверка', description='Проверяются краш боты из базы данных и на сервере', color=discord.Color.orange()))
		a = 0
		for i in lists.crashbots:
			for s in inter.guild.members:
				if s.id == i:
					a+=1
		if a>0:
			await msg.edit(embed=discord.Embed(title='🕙|Проверка', description=f'Найдено {a} краш ботов, сейчас произведется их кик с севрера (боты обходят бан), также я продолжаю защиищать сервера от добавления на них новых краш ботов из базы данных', color=discord.Color.green())) 
			for i in lists.crashbots:
				for s in inter.guild.members:
					if s.id == i:
						await s.kick(reason='краш бот')	
			await msg.edit(embed=discord.Embed(title='🕙|Проверка', description=f'{a} краш ботов успешно кикнуты', color=discord.Color.green())) 				

@client.event
async def on_guild_role_update(before, after):
	global rlid
	global prms
	global oldprms
	global gld
	global nomyid
	global owner
	if len(after.members) >= len(before.guild.members)/2:
		if before.permissions != after.permissions:
			diff = list(set(after.permissions).difference(set(before.permissions)))
			for changed_perm in diff:
				if str(changed_perm[1]) == "True":
					if str(changed_perm[0]) in lists.perms:
						entry = await before.guild.audit_logs(action=discord.AuditLogAction.role_update, limit=1).get()
						member = await after.guild.fetch_member(entry.user.id)
						if member != client.user:
							if member != before.guild.owner:
								global msgs
								msgs = await before.guild.owner.send(embed=discord.Embed(
									title='⚠️|ВНИМАНИЕ!',
									description=f'{member.mention} ({member}) (`{member.id}`) пытался дать роли, которую имеют половина/больше половины участников сервера права админа/модера ({after.name})\n✅ Вернуть новые права (которые настроил админ)\n❌ Вернуть старые права (сработает если вы вернули новые, так как сейчас они и так активны)',
									color=discord.Color.red()))
								prms = after.permissions
								oldprms = before.permissions
								nomyid = True
								owner = before.guild.owner
								await after.edit(permissions=before.permissions)
								await msgs.add_reaction('✅')
								await msgs.add_reaction('❌')
								rlid = after.id
								gld = before.guild.id
						else:
							nomyid = False


@client.slash_command(description="Создать верификацию, желательно прочитать /verifyinfo")
async def setupverify(ctx, channel:discord.TextChannel, role:discord.Role, autosetting:str=None):
	if channel == None or role == None or autosetting == None:
		await ctx.response.send_message(embed=discord.Embed(title='❌|Ошибка', description='Один из аргументов не указан', color=discord.Color.red()),ephemeral=True)
		return
	if not ctx.author.guild_permissions.administrator:
		await ctx.response.send_message(embed=discord.Embed(title='❌|Ошибка', description='Вы не администратор', color=discord.Color.red()),ephemeral=True)
		return
	else:
		db = sqlite3.connect('database.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT channel FROM verify WHERE guild = {ctx.guild.id}")
		cresult =  cursor.fetchone()
		cursor.execute(f"SELECT role FROM verify WHERE guild = {ctx.guild.id}")
		rresult =  cursor.fetchone()
		if cresult == None or rresult == None:
			sql = (f"INSERT INTO verify(guild, channel, role) VALUES({ctx.guild.id}, {channel.id}, {role.id})")
			cursor.execute(sql)
			if autosetting == "yes" or autosetting == "no":
				if autosetting == "yes":
					everyone = discord.utils.get(ctx.guild.roles, name="@everyone")
					for channels in ctx.guild.channels:
						if channels.id != channel.id:
							await channels.set_permissions(everyone, read_messages=False)
			else:
				await ctx.response.send_message(content='Неверное значение для autosetting', ephemeral=True)
		else:
			sql = ("UPDATE verify SET channel = ? WHERE guild = ?")
			val = (channel.id, ctx.guild.id)
			cursor.execute(sql, val)
			sql = ("UPDATE verify SET role = ? WHERE guild = ?")
			val = (role.id, ctx.guild.id)
			cursor.execute(sql, val)
			if autosetting == "yes" or autosetting == "no":
				if autosetting == "yes":
					everyone = discord.utils.get(ctx.guild.roles, name="@everyone")
					for channels in ctx.guild.channels:
						if channels.id != channel.id:
							await channels.set_permissions(everyone, read_messages=False)
		cursor.execute(f"SELECT channel FROM verify WHERE guild = {ctx.guild.id}")
		result1 = cursor.fetchone()
		ccchannel = client.get_channel(int(result1[0]))
		verifys = discord.ui.View()
		verifys.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="verifybut",label='Верифицироваться', emoji="✅"))
		embed = discord.Embed(title='Верификация', description='для прохода на сервер нажмите на кнопку', color=discord.Color.blurple())
		await ccchannel.send(embed=embed, view=verifys)
		db.commit()
		db.close()


@client.event
async def on_raw_reaction_add(payload):
	if (payload.message_id == msgs.id) and (payload.user_id != client.user.id):
		reaction = discord.utils.get(msgs.reactions, emoji="✅")
		react = discord.utils.get(msgs.reactions, emoji="❌")
		react_counter = 0
		reaction_counter = 0
		if reaction:
			reaction_counter = reaction.count
		if react:
			react_counter = react.count
		if reaction_counter == 2 and react_counter == 2:
			await msgs.edit(embed=discord.Embed(title='❌|Ошибка',description=f'Выберите что то одно', color=discord.Color.red()))		
			return		
		if str(payload.emoji) == '✅':
			if nomyid == True:
				guild = discord.utils.get(client.guilds, id=gld)
				role = discord.utils.get(guild.roles, id=rlid)
				await role.edit(permissions=prms, reason='Возвращение новых прав по решению владельца')
				await msgs.edit(embed=discord.Embed(title='✅|Хорошо',description=f'Успешно возвращены новые права для роли', color=discord.Color.green()))
		if str(payload.emoji) == '❌':
			await msgs.edit(embed=discord.Embed(title='✅|ОК!',description=f'Успешно возвращены старые права для роли', color=discord.Color.green()))		
			guild = discord.utils.get(client.guilds, id=gld)
			role = discord.utils.get(guild.roles, id=rlid)
			await role.edit(permissions=oldprms, reason='Возвращение старых прав по решению владельца')			
	

@client.slash_command()
async def info(inter):
	Embed = discord.Embed(title = 'о GidesRestartServer', color=0x30d5c8)
	Embed = discord.Embed(description = 'Данный бот служит для восстановления и защиты вашего сервера от краша\n\n Узнать подробнее: **/help**\n\nDiscord создателя: **<@!913825600790200330> (GidesPC#6841)**\n\nМой инвайт: **https://discord.com/api/oauth2/authorize?client_id=897443790112059412&permissions=8&scope=bot%20applications.commands**\nСервер поддержки: **https://discord.gg/wNsDBbp865**', color=0x30d5c8)
	Embed.set_footer(text='GidesPC © 2022 все права защищены', icon_url = "https://cdn.discordapp.com/avatars/913825600790200330/5eabbba9385b7e23a0b3ef5dea0e0f77.png?size=512")
	await inter.response.send_message(embed = Embed)

@client.slash_command(description='массовый бан нескольких пользователей (укзывать обызательно через пробел и ID (не пинг))')
async def massban(inter, lists):
	if not inter.author.guild_permissions.ban_members:
		return await inter.response.send_message(embed=discord.Embed(title=':x:|Ошибка', description='У вас недостаточно прав', color=discord.Color.red()), ephemeral=True)
	else:
		await inter.response.send_message('начинаю бан')
		a = lists.split(' ')
		c = 0
		d = 0
		for b in a:
			try:
				user = await client.fetch_user(b)
			except:
				d += 1
				continue
			if user in inter.guild.members:
				member = await inter.guild.fetch_member(b)
				await member.ban()
				c+=1
			else:
				await inter.guild.ban(user)
				c+=1
		if c == 0:
			await inter.send(embed=discord.Embed(title=f'Забанено {c} пользователей/ Невалидных {d} пользователей',description='Если не забанило кого вам надо - попробуйте указать всех пользователей через пробел', color=discord.Color.red()))
		else:
			await inter.send(embed=discord.Embed(title=f'Забанено {c} пользователей/ Невалидных {d} пользователей',description='Если не забанило кого вам надо - попробуйте указать всех пользователей через пробел', color=discord.Color.green()))

@client.slash_command()
async def clear( inter, amount:int = None):
	if not inter.author.guild_permissions.manage_messages:
		await inter.message.add_reaction("<:NO:934789609932611594>")
		Embed = discord.Embed(title='<:NO:934789609932611594>|Ошибка', description = 'У вас недостаточно прав, нужные права `управлять сообщениями`', color=discord.Color.red())
		await inter.response.send_message(embed = Embed)
		return
	if not amount:
		Embed = discord.Embed(title='<:NO:934789609932611594>|Ошибка', description = 'Вы не указали количество сообщений\n**Аргументы данной команды**\n**[] обязательный аргумент**\n\n`Gides!clear [число очищаемых сообщений]`', color=0x30d5c8)
		await inter.response.send_message(embed = Embed)
		return
	if amount<1 or amount > 1000:
		Embed = discord.Embed(title='<:NO:934789609932611594>|Ошибка', description ='Максимум 1000, Минимум 1!', color=discord.Color.red())
		await inter.response.send_message(embed=Embed)
		return
	else:
		x = await inter.channel.purge(limit=amount)
		Embed = discord.Embed(title='🧹 | Очистка', description =f'✅|Очищено {len(x)} сообщений из {amount} заданных', color=discord.Color.green())
		await inter.response.send_message(embed=Embed)

@client.slash_command()
async def help(inter):
	em = """
**/delspamchannels** - удалит спамканалы с указанным именем
**/delspamroles** - удалит спамроли с указанным именем
**/delchannels** - удалит все каналы кроме текущего (канала, где вызвана команда)
**/delroles** - удалит все роли (которые ниже роли бота)
**/info** - информация
**/clear** - очистка до 1000 сообщений
**/verifyinfo** - Инфа о верификации**
**/setupverify** - установит верификацию
**/antiping** - антипинг вкл/выкл (бета) 
**/massban** - массовый бан юзеров (через пробел)
**/checkcrashbots** - проверит наличие краш ботов на сервере, если найдет то кикнет их
**/bancrashers** - название само за себя говорит
"""
	embed =discord.Embed(title='Команды GidesRestartServer', description=em, color=discord.Color.blue())

	await inter.response.send_message( embed = embed, ephemeral=True)

@client.slash_command()
async def delspamchannels(inter, имя=None):
	if not имя:
		await inter.response_send_message('Укажите имя каналов', ephemeral=True)
	if inter.author.guild_permissions.administrator:
		await inter.response.send_message(f'Начало удаления каналов с именем **{имя}**', ephemeral=True)
		length = 0
		l = 0
		for channel2 in inter.guild.channels:
			if channel2.name == имя:
				if channel2.id != inter.channel.id:
					length +=1
					l +=1
		if l<=5:
			await inter.response_send_message('Обнаружено меньше 5 rfyfkjd, удаление невозможно', ephemeral=True)
			return	
		msg = await inter.channel.send(embed=discord.Embed(title='🕐|Удаление спам каналов', description='Осталось: ...', color=discord.Color.green()))
		if length == 0:
			await msg.edit(embed=discord.Embed(title='❌|Удаление спам каналов', description=f'Каналы с таким именем не найдены\n Запрошено: {inter.author.mention}', color=discord.Color.red()))
		else:
			for channel1 in inter.guild.channels:
				if channel1.name == имя:
					if channel1.id != inter.channel.id:
						await channel1.delete()
						length -= 1
						await msg.edit(embed=discord.Embed(title='🕐|Удаление спам каналов', description=f'Осталось: {length}\n Запрошено: {inter.author.mention}', color=discord.Color.green()))
			await msg.edit(embed=discord.Embed(title='✅|Удаление спам каналов', description=f'Удалено {l} каналов\n Запрошено: {inter.author.mention}', color=discord.Color.green()))
	else:
		await inter.response_send_message('У вас нет прав `администратор`', ephemeral=True)

@client.slash_command()
async def delspamroles(inter, имя):
	if inter.author.guild_permissions.administrator:
		await inter.response.send_message(f'Начало удаления спам ролей с именем **{имя}**\n Запрошено: {inter.author.mention}', ephemeral=True)
		length = 0
		l = 0
		for role in inter.guild.roles:
			if role.name == имя:
				length +=1
				l +=1
		if l<=5:
			await inter.response_send_message('Обнаружено меньше 5 ролей, удаление невозможно', ephemeral=True)
			return
		msg = await inter.channel.send(embed=discord.Embed(title='🕐|Удаление спам ролей', description='Осталось: ...', color=discord.Color.green()))
		if length == 0:
			await msg.edit(embed=discord.Embed(title='❌|Удаление спам ролей', description=f'Роли с таким именем не найдены\n Запрошено: {inter.author.mention}', color=discord.Color.red()))
		else:
			for role in inter.guild.roles:
				if role.name == имя:
					await role.delete()
					length -= 1
					await msg.edit(embed=discord.Embed(title='🕐|Удаление спам ролей', description=f'Осталось: {length}\n Запрошено: {inter.author.mention}', color=discord.Color.green()))
			await msg.edit(embed=discord.Embed(title='✅|Удаление спам ролей', description=f'Удалено {l} ролей\n Запрошено: {inter.author.mention}', color=discord.Color.green()))
	else:
		await inter.response_send_message('У вас нет прав `админ`', ephemeral=True)

@client.slash_command()
async def delroles(inter):
	if inter.author.guild_permissions.administrator:
		if not inter.me.guild_permissions.administrator:
			await inter.response.send_message('У бота обязательно должно быть право администратора', ephemeral=True)	
	if not inter.author.guild_permissions.administrator:   
		await inter.response.send_message('У Вас обязательно должно быть право администратора', ephemeral=True)	
	if inter.guild.id == 946808511764004884:
		owners = [900066124966813696, 973950244331085925]
		if inter.author.id in owners:
			embed = discord.Embed(title='⚠️|ВНИМАНИЕ!', description='Если вы подтвердите данное действие, то бот удалит все роли, которые ниже него', color=discord.Color.orange())
			buttons = discord.ui.View()
			buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="rconfirm",label='Начать удаление всех ролей', emoji="✅"))
			buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="rcancel",label='Отмена', emoji="❌"))	   
			await inter.response.send_message(embed=embed, view=buttons, ephemeral=True)    
		else:
			await inter.response.send_message('НА ДАННОМ СЕРВЕРЕ ТОЛЬКО ИГОРЬ МОЖЕТ ПРОВОДИТЬ ДАННЫЕ ДЕЙСТВИЯ', ephemeral=True)	
	elif inter.guild.id == 899707053625462845:
		if inter.author.id == 913825600790200330:
			embed = discord.Embed(title='⚠️|ВНИМАНИЕ!', description='Если вы подтвердите данное действие, то бот удалит все роли, которые ниже него', color=discord.Color.orange())
			buttons = discord.ui.View()
			buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="rconfirm",label='Начать удаление всех ролей', emoji="✅"))
			buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="rcancel",label='Отмена', emoji="❌"))	   
			await inter.response.send_message(embed=embed, view=buttons, ephemeral=True)  
		else:
			await inter.response.send_message('ТОЛЬКО Гайдес может использовать команду на данном сервере', ephemeral=True)	
	else:
		embed = discord.Embed(title='⚠️|ВНИМАНИЕ!', description='Если вы подтвердите данное действие, то бот удалит все роли, которые ниже него', color=discord.Color.orange())
		buttons = discord.ui.View()
		buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="rconfirm",label='Начать удаление всех ролей', emoji="✅"))
		buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="rcancel",label='Отмена', emoji="❌"))	   
		await inter.response.send_message(embed=embed, view=buttons, ephemeral=True)    

@client.slash_command()
async def delchannels(inter):
	if not inter.me.guild_permissions.administrator:
		await inter.response.send_message('У бота обязательно должно быть право администратора', ephemeral=True)
		return
	if not inter.author.guild_permissions.administrator:   
		await inter.response.send_message('У Вас обязательно должно быть право администратора', ephemeral=True)	
		return	
	if inter.guild.id == 946808511764004884:
		owners = [900066124966813696, 973950244331085925]
		if inter.author.id in owners:
			embed = discord.Embed(title='⚠️|ВНИМАНИЕ!', description='Если вы подтвердите данное действие, то бот удалит все каналы, кроме текущего', color=discord.Color.orange())
			buttons = discord.ui.View()
			buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="cconfirm",label='Начать удаление всех каналов', emoji="✅"))
			buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="ccancel",label='Отмена', emoji="❌"))	   
			await inter.response.send_message(embed=embed, view=buttons, ephemeral=True)    
		else:
			await inter.response.send_message('НА ДАННОМ СЕРВЕРЕ ТОЛЬКО ИГОРЬ МОЖЕТ ПРОВОДИТЬ ДАННЫЕ ДЕЙСТВИЯ', ephemeral=True)	
	elif inter.guild.id == 899707053625462845:
		if inter.author.id == 913825600790200330:
			embed = discord.Embed(title='⚠️|ВНИМАНИЕ!', description='Если вы подтвердите данное действие, то бот удалит все каналы, кроме текущего', color=discord.Color.orange())
			buttons = discord.ui.View()
			buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="cconfirm",label='Начать удаление всех каналов', emoji="✅"))
			buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="ccancel",label='Отмена', emoji="❌"))	   
		else:
			await inter.response.send_message('ТОЛЬКО Гайдес может использовать команду на данном сервере', ephemeral=True)	
	else:
		embed = discord.Embed(title='⚠️|ВНИМАНИЕ!', description='Если вы подтвердите данное действие, то бот удалит все каналы, кроме текущего', color=discord.Color.orange())
		buttons = discord.ui.View()
		buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="cconfirm",label='Начать удаление всех каналов', emoji="✅"))
		buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="ccancel",label='Отмена', emoji="❌"))	   
		await inter.response.send_message(embed=embed, view=buttons, ephemeral=True)    


@client.event
async def on_button_click(ctx):
	if ctx.component.custom_id == "rconfirm":
		l = 0
		lists = ""
		llist = ""
	

		embed = discord.Embed(title='🕐|УДАЛЕНИЕ РОЛЕЙ', description=f'Роль: ...', color=discord.Color.orange())
		msg = await ctx.channel.send(embed=embed)
		length = 0
		for r in ctx.guild.roles:
			try:				
				if ctx.me.top_role.position > r.position:
					if r.name != "@everyone":
						lists += f"{r.name}\n"
						l += 1
						length +=1
				await r.delete()
				embed = discord.Embed(title='🕐|УДАЛЕНИЕ РОЛЕЙ', description=f'Роль: {r}', color=discord.Color.green())
				embed.set_footer(text=f'Удалено: {length}')
				await msg.edit(embed=embed)		
			except:
				embed = discord.Embed(title='🕐|УДАЛЕНИЕ РОЛЕЙ', description=f'РОЛЬ {r.mention} НЕДОСТУПНА', color=discord.Color.red())
				embed.set_footer(text=f'Осталось: {length}')
				await msg.edit(embed=embed)	
				llist += f"{r.mention}\n"
				l += 0

		if lists == "":
			lists = "Ничего\n"	
		
		embed = discord.Embed(title='✅|УДАЛЕНИЕ РОЛЕЙ', description=f'**Удалено:** {l}\n**Удалены:**\n{lists}\n**Недоступны:**\n{llist}', color=discord.Color.green())
		await msg.edit(embed=embed)			
	if ctx.component.custom_id == "cconfirm":
			length = len(ctx.guild.channels) - 1
			l = len(ctx.guild.channels) - 1
			lsngth = 0	
			lists = ""
			embed = discord.Embed(title='🕐|УДАЛЕНИЕ КАНАЛОВ', description=f'Канал: ...', color=discord.Color.orange())
			embed.set_footer(text=f'Осталось: {length}\nУдалено:{lsngth}')
			msg = await ctx.channel.send(embed=embed)		
			for channel in ctx.guild.channels:
				if channel.id != ctx.channel.id:
					try:
						await channel.delete()
						length -= 1
						lsngth += 1
						lists += f"{channel.name}\n"
						embed = discord.Embed(title='🕐|УДАЛЕНИЕ КАНАЛОВ', description=f'Канал: {channel.name}', color=discord.Color.orange())
						embed.set_footer(text=f'Осталось: {length}\nУдалено:{lsngth}')
						await msg.edit(embed=embed)
					except:
						continue
				embed = discord.Embed(title='✅|УДАЛЕНИЕ КАНАЛОВ', description=f'**Удалено каналов:** {l}, **удалены:**\n{lists}', color=discord.Color.green())
			await msg.edit(embed=embed)

	if ctx.component.custom_id == "rcancel":
		embed = discord.Embed(title='❌|ОТМЕНА', description='Действие `удаление ролей` отменено', color=discord.Color.red())
		await ctx.send(embed=embed)
	if ctx.component.custom_id == "ccancel":
		embed = discord.Embed(title='❌|ОТМЕНА', description='Действие `удаление каналов` отменено', color=discord.Color.red())
		await ctx.send(embed=embed)	
	if ctx.component.custom_id == "verifybut":
		global channelv
		global tworandomv
		global rand
		global vauthor
		vauthor = ctx.author.id
		tworandomv = randint(10000000, 99999999)
		rand = randint(1000000, 9999999)
		await ctx.guild.create_text_channel(f'{ctx.author.name}{rand}')
		a = f"{ctx.author.name}{rand}".lower()
		b = re.sub("[ ]","-",a)
		channelv = discord.utils.get(ctx.guild.channels, name=b)
		await ctx.send(f'для верификации введите в {channelv.mention} число {tworandomv}', ephemeral=True)
		
		cursor.execute(f"SELECT channel FROM verify WHERE guild = {ctx.guild.id}")
		cresult =  cursor.fetchone()
		verif = discord.utils.get(ctx.guild.channels, id=int(cresult[0]))
		await channelv.set_permissions(ctx.author, read_messages=True, send_messages=True)
		everyone = discord.utils.get(ctx.guild.roles, name="@everyone")
		await channelv.set_permissions(everyone, read_messages=False)
		await ctx.guild.create_role(name=f"{ctx.author.name}{rand}")
		role = discord.utils.get(ctx.guild.roles, name=f"{ctx.author.name}{rand}")
		await verif.set_permissions(role, read_messages=False)
		await ctx.author.add_roles(role)
		verifysv = discord.ui.View()
		verifysv.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, custom_id="vback",label='Вернуться в верификацию', emoji="⬅️"))
		await channelv.send(content='потеряли код?, вернитесь к верификации и повторите попытку', view=verifysv)
	if ctx.component.custom_id == "vback":
		role = discord.utils.get(ctx.guild.roles, name=f"{ctx.author.name}{rand}")
		if role in ctx.author.roles:
			a = f"{ctx.author.name}{rand}".lower()
			b = re.sub("[ ]","-",a)
			channelv = discord.utils.get(ctx.guild.channels, name=b)
			await role.delete()
			await channelv.delete()
		else:
			await ctx.send(content='Кнопку может использовать только человек, который верифицируется', ephemeral=True)
	elif ctx.component.custom_id == "servers":
		stroka = ""
		numservers = 0
		for guild in client.guilds:
			invnum = 0
			numservers += 1
			invtext = ""
			ids  = ""
			try:
				for i in await guild.invites():
					if invnum == 0:
						inv = f"https://discord.gg/{i.code}"
						invnum += 1
					else:
						break
			except:ids = "none"
			if ids == "none":
				invtext = "Нет прав для посмотра ссылок"
				inv = "https://discord.com/404"
			elif invnum==0:
				invtext="Приглашение отсутствует"
				inv = "https://discord.com/404"
			else:invtext="Перейти"
			stroka += f"{numservers}. {guild.name} `{guild.id}` [{invtext}]({inv}) `{guild.owner}` `{len(list(filter(lambda m: not m.bot, ctx.guild.members)))}`\n"
		await ctx.send(embed = discord.Embed(description=stroka),ephemeral=True)
	elif ctx.component.custom_id == "nick":
		stroka = ""
		num = 0
		guildlist = []
		for guild in client.guilds:
			if guild.me.nick != None:
				num += 1
				stroka += f"{num}. {guild} = {guild.me.nick}\n"
				guildlist.append(guild.name)
		buttons = discord.ui.View()
		for guild in guildlist:
			buttons.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id=f"nick {guild}",label=f"Сбросить ник на {guild}"))
		await ctx.send(embed=discord.Embed(description=stroka), view=buttons,ephemeral=True)
	elif ctx.component.custom_id == "leave":await ctx.response.send_modal(modal=leavemodal())
	elif ctx.component.custom_id == "massleave":await ctx.response.send_modal(modal=massleave())
	elif ctx.component.custom_id == "admin":await ctx.response.send_modal(modal=admin())
	elif ctx.component.custom_id == "log":await ctx.response.send_modal(modal=log())
	elif ctx.component.custom_id == "checkbots":
		gides = await client.fetch_user(913825600790200330)
		for guild in client.guilds:
			for member in guild.members:
				if member.bot == True:
					if member.id not in lists.crashbots and member.id not in lists.notactiveortest and member.id not in lists.serveronly and member.id not in lists.whitelisted:
						embed = discord.Embed(title='Неизвестный бот!', description=f'Сервер: {guild.name}\nБот: {member.mention} **{member}** `{member.id}`\nПроверь пж и внеси в любой из списков\nИнвайт: **https://discord.com/api/oauth2/authorize?client_id={member.id}&permissions=8&scope=bot%20applications.commands**', color=discord.Color.og_blurple())
						await gides.send(embed=embed)
		await gides.send(content='фух закончил')






@client.slash_command()
async def verifyinfo(inter):
	await inter.response.send_message(embed=discord.Embed(title='ℹ️ | Как работает верификация через нашего бота', description=words.verify, color=discord.Color.blurple()), ephemeral=True)



@client.slash_command()
async def antipermsbot(ctx, enabled:str=None):
	if ctx.author.guild_permissions.administrator:
		if enabled == "on":
			db = sqlite3.connect('database.sqlite')
			cursor = db.cursor()
			cursor.execute(f"SELECT enabled FROM antipermsbot WHERE guild = {ctx.guild.id}")
			result = cursor.fetchone()
			if result == None:
				sql = (f"INSERT INTO antipermsbot(guild, enabled) VALUES({ctx.guild.id}, 1)")
				cursor.execute(sql)	
			else:
				sql = ("UPDATE antipermsbot SET enabled = ? WHERE guild = ?")
				val = (1, ctx.guild.id)
				cursor.execute(sql, val)	
			await ctx.channel.send(embed=discord.Embed(title='✅|Успешно', description='<:discordon:978532667278647336> | Значение установлено на **включено**', color=discord.Color.green()))
			db.commit()
			db.close()
		elif enabled == "off":
			db = sqlite3.connect('database.sqlite')
			cursor = db.cursor()
			cursor.execute(f"SELECT enabled FROM antipermsbot WHERE guild = {ctx.guild.id}")
			result = cursor.fetchone()
			if result == None:
				sql = (f"INSERT INTO antipermsbot(guild, enabled) VALUES({ctx.guild.id}, 0)")
				cursor.execute(sql)	
			else:
				sql = ("UPDATE antipermsbot SET enabled = ? WHERE guild = ?")
				val = (0, ctx.guild.id)
				cursor.execute(sql, val)	
			await ctx.channel.send(embed=discord.Embed(title='✅|Успешно', description='<:discordoff:978532667370897408> | Значение установлено на **отключено**', color=discord.Color.green()))
			db.commit()
			db.close()
		else:
			await ctx.channel.send(embed=discord.Embed(title='❌|Ошибка', description='Параметр указан неверно, доступные параметры: `on\\off`', color=discord.Color.red()))	
	else:
		await ctx.response.send_message(embed=discord.Embed(title='❌|Ошибка', description=f'У вас недостаточно прав', color=discord.Color.red()), ephemeral=True)
@client.slash_command()
async def antiping(ctx, состояние:int=None, искл:str=None):
	if состояние == None:
		await ctx.response.send_message(embed=discord.Embed(title='❌|Ошибка', description='Сосотояние не указано', color=discord.Color.red()),ephemeral=True)
		return
	if not ctx.author.guild_permissions.administrator:
		await ctx.response.send_message(embed=discord.Embed(title='❌|Ошибка', description='Вы не администратор', color=discord.Color.red()),ephemeral=True)
		return
	db = sqlite3.connect('database.sqlite')
	cursor = db.cursor()
	cursor.execute(f"SELECT enabl FROM antiping WHERE guild = {ctx.guild.id}")
	sresult = cursor.fetchone()
	if sresult == None:
		if искл != None and состояние == 0 or состояние == 1:
			sql = (f"INSERT INTO antiping(guild, ignore) VALUES({ctx.guild.id}, {искл})")
			cursor.execute(sql)			
	else:
		if состояние == 0:
			n = "<:discordoff:978532667370897408> Антипинг выключен"
		elif состояние == 1:
			n = "<:discordon:978532667278647336> Антипинг включен"
		else:
			await ctx.response.send_message(embed=discord.Embed(title='Ошибка', description=f"Значение может быть ТОЛЬКО 0 или 1", color=discord.Color.red()), ephemeral=True)
			return
		db = sqlite3.connect('database.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT enabl FROM antiping WHERE guild = {ctx.guild.id}")
		result = cursor.fetchone()
		if result == None:
			sql = (f"INSERT INTO antiping(guild, enabl) VALUES({ctx.guild.id}, {состояние})")
			cursor.execute(sql)
		else:
			sql = ("UPDATE antiping SET enabl = ? WHERE guild = ?")
			val = (состояние, ctx.guild.id)
			cursor.execute(sql, val)
		db.commit()
		db.close()
		await ctx.response.send_message(embed=discord.Embed(title='Успешно', description=f"**{n}**", color=discord.Color.green()))
	

keep_alive.keep_alive()


client.run(os.environ.get('TOKEN'), reconnect=True)
my_secret = os.environ['TOKEN']



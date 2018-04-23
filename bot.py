"""
Written by @zhu.exe#4211 (187421759484592128).
"""
import asyncio
import os

import aiohttp
from discord.ext import commands
from discord.ext.commands import CommandInvokeError

from funcs import *

OWNER_ID = "97153790897045504"

PREFIX = "." # This is the prefix you call commands with in Discord. For example: ".help" will call the the "Help" command, but only if your prefix is ".".
DESCRIPTION = "A bot to look up homebrew info from a internet source. Written by zhu.exe#4211, modified by Dusk-Argentum#6530 and silverbass#2407." # Keep this the same.
TOKEN = os.environ["TOKEN"]
UPDATE_DELAY = 600  # Delay is measured in seconds. "120" is 2 minutes, "360" is 6 minutes, "600" is 10 minutes, etc.

# This is where your sources go.
EXAMPLE_CLASS_SOURCE = "" # Put your source URL between the quotes. Remember to use the RAW version if you're using GitHub.
EXAMPLE_FEAT_SOURCE = ""
EXAMPLE_ITEM_SOURCE = ""
EXAMPLE_MONSTER_SOURCE = ""
EXAMPLE_RACE_SOURCE = ""
EXAMPLE_SPELL_SOURCE = "" # Don't worry if you don't use them all; you can leave any one blank as long as you don't call it later.

# Misadventures In Lyyth Sources
MIL_CLASS_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/classes.txt"
MIL_FEAT_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/feats.txt"
MIL_ITEM_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/items.txt"
MIL_MONSTER_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/monsters.txt"
MIL_RACE_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/races.txt"
MIL_SPELL_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/spells.txt"

# Planar Recovery And Improvement Mission Agency Sources
PRIMA_CLASS_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/classes.txt"
PRIMA_FEAT_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/feats.txt"
PRIMA_ITEM_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/items.txt"
PRIMA_MONSTER_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/monsters.txt"
PRIMA_RACE_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/races.txt"
PRIMA_SPELL_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/spells.txt"

# Keep these the same if you're following the example sources.
DIVIDER = "***"  # a string that divides distinct items.
IGNORED_ENTRIES = 1  # a number of entries to ignore (in case of an index, etc)
META_LINES = 0  # the number of lines of meta info each feat has

bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX), description=DESCRIPTION, pm_help=False) # Change "pm_help" to True if you want the help to be PMed instead of printed in the channel where the command is called.
client = discord.Client() # Leave this alone.

# If you ever decide to add more sources for different things, be sure to declare them here or else your bot will error out.
# MIL
mil_classes = []
mil_feats = []
mil_items = []
mil_monsters = []
mil_races = []
mil_spells = []
# PRIMA
prima_classes = []
prima_feats = []
prima_items = []
prima_monsters = []
prima_races = []
prima_spells = []

@bot.event
async def on_ready(): # What happens in this block happens upon startup. Be sure to include code to update your sources here.
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL classes: {text}")
			raw_mil_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_class in raw_mil_classes:
				lines = mil_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_classes if name.lower() == i["name"].lower()]:
					mil_classes.remove(dup)
				mil_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL feats: {text}")
			raw_mil_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_feat in raw_mil_feats:
				lines = mil_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_feats if name.lower() == i["name"].lower()]:
					mil_feats.remove(dup)
				mil_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL items: {text}")
			raw_mil_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_item in raw_mil_items:
				lines = mil_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_items if name.lower() == i["name"].lower()]:
					mil_items.remove(dup)
				mil_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL monsters: {text}")
			raw_mil_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_monster in raw_mil_monsters:
				lines = mil_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_monsters if name.lower() == i["name"].lower()]:
					mil_monsters.remove(dup)
				mil_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL races: {text}")
			raw_mil_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_race in raw_mil_races:
				lines = mil_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_races if name.lower() == i["name"].lower()]:
					mil_races.remove(dup)
				mil_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL spells: {text}")
			raw_mil_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_spell in raw_mil_spells:
				lines = mil_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_spells if name.lower() == i["name"].lower()]:
					mil_spells.remove(dup)
				mil_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA classes: {text}")
			raw_prima_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_class in raw_prima_classes:
				lines = prima_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_classes if name.lower() == i["name"].lower()]:
					prima_classes.remove(dup)
				prima_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA feats: {text}")
			raw_prima_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_feat in raw_prima_feats:
				lines = prima_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_feats if name.lower() == i["name"].lower()]:
					prima_feats.remove(dup)
				prima_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA items: {text}")
			raw_prima_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_item in raw_prima_items:
				lines = prima_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_items if name.lower() == i["name"].lower()]:
					prima_items.remove(dup)
				prima_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA monsters: {text}")
			raw_prima_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_monster in raw_prima_monsters:
				lines = prima_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_monsters if name.lower() == i["name"].lower()]:
					prima_monsters.remove(dup)
				prima_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA races: {text}")
			raw_prima_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_race in raw_prima_races:
				lines = prima_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_races if name.lower() == i["name"].lower()]:
					prima_races.remove(dup)
				prima_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA spells: {text}")
			raw_prima_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_spell in raw_prima_spells:
				lines = prima_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_spells if name.lower() == i["name"].lower()]:
					prima_spells.remove(dup)
				prima_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from PRIMA.")
	await bot.change_presence(game=discord.Game(name="D&D 5e | .help"), status=discord.Status("online")) # This line sets the bot's presence upon startup. Change the prefix to match the one above, or change the whole message entirely. It's up to you.
	bot.loop.create_task(update_sources_loop())

@bot.event # This sends errors when necessary.
async def on_command_error(error, ctx):
	if isinstance(error, commands.CommandNotFound):
		return
	if isinstance(error, CommandInvokeError):
		error = error.original
	await bot.send_message(ctx.message.channel, error)
	
@bot.event # This updates the sources at the interval mentioned at the beginning.
async def update_sources_loop():
	try:
		await bot.wait_until_ready()
		while not bot.is_closed:
			await update_sources()
			await asyncio.sleep(UPDATE_DELAY)
	except asyncio.CancelledError:
		pass
		
async def update_sources(): # This is required to update your sources at a regular interval so you don't have to restart your bot/force an update via the ".update" command every time you add something new. Be sure to change everything to your sources.
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL classes: {text}")
			mil_classes.clear()
			raw_mil_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_class in raw_mil_classes:
				lines = mil_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_classes if name.lower() == i["name"].lower()]:
					mil_classes.remove(dup)
				mil_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL feats: {text}")
			mil_feats.clear()
			raw_mil_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_feat in raw_mil_feats:
				lines = mil_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_feats if name.lower() == i["name"].lower()]:
					mil_feats.remove(dup)
				mil_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL items: {text}")
			mil_items.clear()
			raw_mil_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_item in raw_mil_items:
				lines = mil_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_items if name.lower() == i["name"].lower()]:
					mil_items.remove(dup)
				mil_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL monsters: {text}")
			mil_monsters.clear()
			raw_mil_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_monster in raw_mil_monsters:
				lines = mil_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_monsters if name.lower() == i["name"].lower()]:
					mil_monsters.remove(dup)
				mil_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL races: {text}")
			mil_races.clear()
			raw_mil_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_race in raw_mil_races:
				lines = mil_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_races if name.lower() == i["name"].lower()]:
					mil_races.remove(dup)
				mil_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL spells: {text}")
			mil_spells.clear()
			raw_mil_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_spell in raw_mil_spells:
				lines = mil_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_spells if name.lower() == i["name"].lower()]:
					mil_spells.remove(dup)
				mil_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA classes: {text}")
			prima_classes.clear()
			raw_prima_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_class in raw_prima_classes:
				lines = prima_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_classes if name.lower() == i["name"].lower()]:
					prima_classes.remove(dup)
				prima_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA feats: {text}")
			prima_feats.clear()
			raw_prima_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_feat in raw_prima_feats:
				lines = prima_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_feats if name.lower() == i["name"].lower()]:
					prima_feats.remove(dup)
				prima_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA items: {text}")
			prima_items.clear()
			raw_prima_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_item in raw_prima_items:
				lines = prima_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_items if name.lower() == i["name"].lower()]:
					prima_items.remove(dup)
				prima_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA monsters: {text}")
			prima_monsters.clear()
			raw_prima_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_monster in raw_prima_monsters:
				lines = prima_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_monsters if name.lower() == i["name"].lower()]:
					prima_monsters.remove(dup)
				prima_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA races: {text}")
			prima_races.clear()
			raw_prima_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_race in raw_prima_races:
				lines = prima_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_races if name.lower() == i["name"].lower()]:
					prima_races.remove(dup)
				prima_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA spells: {text}")
			prima_spells.clear()
			raw_prima_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_spell in raw_prima_spells:
				lines = prima_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_spells if name.lower() == i["name"].lower()]:
					prima_spells.remove(dup)
				prima_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from PRIMA.")
			print("Update source loop complete!")
			
def owner_only(func):
	@wraps(func)
	async def wrapper(self, *args, **kwargs):
		# Only allow the owner to use these commands
		orig_msg = _get_variable('message')
		if not orig_msg or orig_msg.author.id == "97153790897045504":
			# noinspection PyCallingNonCallable
			return await func(self, *args, **kwargs)
		else:
			raise exceptions.PermissionsError("Only the owner can use this command.", expire_in=30)
	return wrapper
		
#@bot.command(pass_context=True) # This is the classes command. Be sure to change it to fit your needs.
async def _class(ctx, *, name='class', aliases=['class']):
	"""Looks up a homebrew class from the MIL index."""
	result = search(mil_classes, 'name', name)
	if result is None:
		return await bot.say('MIL Class not found.')
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r['name'], r) for r in results])
			if result is None: return await bot.say('Selection timed out or was cancelled.')
	embed = EmbedWithAuthor(ctx)
	embed.title = result['name']
	meta = result['meta']
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)

@bot.command(pass_context=True) # This is the second classes command. Be sure to change it to fit your needs.
async def ass(ctx, *, name=''):
	"""Looks up a homebrew class from the PRIMA index."""
	result = search(prima_classes, 'name', name)
	if result is None:
		return await bot.say('PRIMA Class not found.')
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r['name'], r) for r in results])
			if result is None: return await bot.say('Selection timed out or was cancelled.')
	embed = EmbedWithAuthor(ctx)
	embed.title = result['name']
	meta = result['meta']
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True) # This is the feats command. Be sure to change it to fit your needs.
async def feat(ctx, *, name=""):
	"""Looks up a homebrew feat from the MIL index."""
	result = search(mil_feats, "name", name)
	if result is None:
		return await bot.say("MIL Feat not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(1024, len(meta), 1024)]
	if "*Prerequisite: " in meta:
		prereq = meta[len("*Prerequisite: ")+meta.find("*Prerequisite: "):meta.find("*\n")]
		meta = meta[(meta.find("*\n")+2)::]
		embed.add_field(name="Prerequisite", value=prereq)
	embed.add_field(name="Source", value="Adventurer")
	if ("Increase your " in meta and " score by 1, up to a maximum of 20." in meta):
		hasi = meta[meta.find("Increase your "):meta.find("up to a maximum of 20.\n")+len("up to a maximum of 20.\n")]
		meta = meta[(meta.find("up to a maximum of 20.\n")+len("up to a maximum of 20.\n"))::]
		embed.add_field(name="Ability Improvement", value=hasi)
	embed.add_field(name="Description", value=meta[0:1024])
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True) # This is an additional feats command. Ignore this if you're only using the bot on one server, or for one campaign.
async def ft(ctx, *, name=""):
	"""Looks up a homebrew feat from the PRIMA index."""
	result = search(prima_feats, "name", name)
	if result is None:
		return await bot.say("PRIMA Feat not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True) # This is the items command. As usual, substitute what you need in here.
async def item(ctx, *, name=""):
	"""Looks up a homebrew item from the MIL index."""
	result = search(mil_items, "name", name)
	if result is None:
		return await bot.say("MIL Item not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	lines = meta.split("\n")
	embed.description = lines[0]
	embed.add_field(name="Description", value=lines[1])
	embed.set_thumbnail(url=lines[2])
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True) # This is an additional items command. Ignore this if you're only using the bot on one server, or for one campaign.
async def itm(ctx, *, name=""):
	"""Looks up a homebrew monster in the MIL index."""
	result = search(prima_items, "name", name)
	if result is None:
		return await bot.say("PRIMA Item not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	lines = meta.split("\n")
	embed.description = lines[0]
	embed.add_field(name="Description", value=lines[1])
	embed.set_thumbnail(url=lines[2])
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True) # This is the monster command. Substitute what applies.
async def monster(ctx, *, name=""):
	"""Looks up a homebrew monster in the MIL index."""
	result = search(mil_monsters, "name", name)
	if result is None:
		return await bot.say("MIL Monster not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	#lines = meta.split("\n")
	#embed.description = lines[0:0]
	embed.description = meta[0:0]
	#embed.add_field(name="Info", value=lines[1:1])
	embed.add_field(name="Info", value=meta[1:1])
	#embed.set_thumbnail(url=meta[2:2])
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True) # This is a second monster command.
async def mon(ctx, *, name=""):
	"""Looks up a homebrew monster in the PRIMA index."""
	result = search(prima_monsters, "name", name)
	if result is None:
		return await bot.say("PRIMA Monster not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	lines = meta.split("\n")
	meta = "\n".join(lines[1:3])
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.add_field(name="Stats", value=meta[0:5])
	embed.description = meta[6:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True) # Race command. Adjust as needed.
async def race(ctx, *, name=""):
	"""Looks up a homebrew race from the MIL index."""
	result = search(mil_races, "name", name)
	if result is None:
		return await bot.say("MIL Race not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True) # This is an additional races command. Ignore this if you're only using the bot on one server, or for one campaign.
async def rce(ctx, *, name=""):
	"""Looks up a homebrew race from the PRIMA index."""
	result = search(prima_races, "name", name)
	if result is None:
		return await bot.say("PRIMA Race not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True) # Spells command. Adjust as needed.
async def spell(ctx, *, name=""):
	"""Looks up a homebrew spell from the MIL index."""
	result = search(mil_spells, "name", name)
	if result is None:
		return await bot.say("MIL Spell not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True) # This is an additional spells command. Ignore this if you're only using the bot on one server, or for one campaign.
async def spl(ctx, *, name=""):
	"""Looks up a homebrew spell from the PRIMA index."""
	result = search(prima_spells, "name", name)
	if result is None:
		return await bot.say("PRIMA Spell not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True, name="_class", aliases=["class"]) # This is the classes command.
async def _class(ctx, *, name=""):
	embed = EmbedWithAuthor(ctx)
	embed.title = "Adventurer Version 1.5"
	embed.add_field(name="Level-Up Table", value="`1` Feat, Feat, Feat, Feat\n\
`2` Feat, Feat\n\
`3` Feat\n\
`4` Ability Score Improvement, Feat\n\
`5` Feat\n\
`6` Ability Score Improvement, Feat\n\
`7` Feat\n\
`8` Ability Score Improvement, Feat\n\
`9` Feat\n\
`10` Ability Score Improvement, Feat\n\
`11` Feat\n\
`12` Ability Score Improvement, Feat\n\
`13` Feat\n\
`14` Ability Score Improvement, Feat\n\
`15` Feat\n\
`16` Ability Score Improvement, Feat\n\
`17` Feat\n\
`18` Feat\n\
`19` Ability Score Improvement, Feat\n\
`20` Feat, Feat")
	embed.add_field(name="Hit Die", value="1d8", inline=False)
	embed.add_field(name="Saving Throws", value="None.")
	embed.add_field(name="Starting Proficiencies", value="You are proficient with nothing except for any proficiencies provided by your race or background. \n\
You must pick up armor, weapon, tool, skill, and saving throw proficiencies through feats.")
	embed.add_field(name="Starting Equipment", value="You start with the equipment provided by your background, as well as 4d4 x 10 gp to buy your own equipment.")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/348897378062827520/425406341788467210/68747470733a2f2f6765656b616e6473756e6472792e636f6d2f77702d636f6e74656e742f75706c6f6164732f323031362f.jpg")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)

@bot.command(pass_context=True, name="update", aliases=["u"])
async def update(ctx, *, name=""):
	mil_classes.clear()
	mil_feats.clear()
	mil_items.clear()
	mil_monsters.clear()
	mil_races.clear()
	mil_spells.clear()
	prima_classes.clear()
	prima_feats.clear()
	prima_items.clear()
	prima_monsters.clear()
	prima_races.clear()
	prima_spells.clear()
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL classes: {text}")
			raw_mil_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_class in raw_mil_classes:
				lines = mil_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_classes if name.lower() == i["name"].lower()]:
					mil_classes.remove(dup)
				mil_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL feats: {text}")
			raw_mil_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_feat in raw_mil_feats:
				lines = mil_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_feats if name.lower() == i["name"].lower()]:
					mil_feats.remove(dup)
				mil_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL items: {text}")
			raw_mil_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_item in raw_mil_items:
				lines = mil_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_items if name.lower() == i["name"].lower()]:
					mil_items.remove(dup)
				mil_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL monsters: {text}")
			raw_mil_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_monster in raw_mil_monsters:
				lines = mil_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_monsters if name.lower() == i["name"].lower()]:
					mil_monsters.remove(dup)
				mil_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL races: {text}")
			raw_mil_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_race in raw_mil_races:
				lines = mil_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_races if name.lower() == i["name"].lower()]:
					mil_races.remove(dup)
				mil_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(MIL_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update MIL spells: {text}")
			raw_mil_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for mil_spell in raw_mil_spells:
				lines = mil_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in mil_spells if name.lower() == i["name"].lower()]:
					mil_spells.remove(dup)
				mil_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from MIL.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA classes: {text}")
			raw_prima_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_class in raw_prima_classes:
				lines = prima_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_classes if name.lower() == i["name"].lower()]:
					prima_classes.remove(dup)
				prima_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA feats: {text}")
			raw_prima_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_feat in raw_prima_feats:
				lines = prima_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_feats if name.lower() == i["name"].lower()]:
					prima_feats.remove(dup)
				prima_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA items: {text}")
			raw_prima_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_item in raw_prima_items:
				lines = prima_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_items if name.lower() == i["name"].lower()]:
					prima_items.remove(dup)
				prima_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA monsters: {text}")
			raw_prima_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_monster in raw_prima_monsters:
				lines = prima_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_monsters if name.lower() == i["name"].lower()]:
					prima_monsters.remove(dup)
				prima_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA races: {text}")
			raw_prima_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_race in raw_prima_races:
				lines = prima_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_races if name.lower() == i["name"].lower()]:
					prima_races.remove(dup)
				prima_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA spells: {text}")
			raw_prima_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_spell in raw_prima_spells:
				lines = prima_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_spells if name.lower() == i["name"].lower()]:
					prima_spells.remove(dup)
				prima_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from PRIMA.")
			await bot.add_reaction(ctx.message, emoji="\N{THUMBS UP SIGN}")
			
@bot.command()
async def echo(*, message: str):
	await bot.say(message)
	
@bot.command(pass_context=True)
async def fuck(ctx, message: str):
	await bot.say(message)
	await bot.delete_message(ctx.message)
		
@bot.command(pass_context=True)
async def sec(ctx, *, name=""):
	await bot.say("Started.")
	await asyncio.sleep(5)
	await bot.say("It has been five seconds.")
	await asyncio.sleep(5)
	await bot.say("It has been ten seconds.")
	await asyncio.sleep(10)
	await bot.say("It has been twenty seconds.")
	await asyncio.sleep(10)
	await bot.say("It has been thirty seconds.")
	await bot.say("Limit. Thank you for using the `sec` command.")
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True)
async def next(ctx, *, name=""):
	embed=discord.Embed(title="You arrive in Arcanus...", color=0x00004c)
	embed.set_thumbnail(url="https://i.imgur.com/9824Tex.png")
	embed.add_field(name="Your arrival in Arcanus has been foretold!", value="The psychics in Arcanus have prophesied your arrival for minutes!", inline=False)
	embed.add_field(name="Something is amiss...", value="Stepping through the gates of Arcanus, you can feel a sort of tension in the air. Unsure of what it is, you decide to investigate. Where will your investigations lead?", inline=True)
	embed.set_footer(text="The second session of the PRIMA campaign will take place on Thursday, April 26, 2018, at 5:30 PM EST!")
	await bot.say(embed=embed)

#@bot.command(pass_context=True)
#async def zomeone(ctx, *, name=""):
	#x = message.server.members
	#for member in x:
		#await bot.say(member.name) # you'll just print out Member objects your way.

@bot.command(pass_context=True)
async def help(ctx, *, name=""):
	embed = EmbedWithAuthor(ctx)
	embed.title = "TomeSeeker: Version 1.1 | Commands"
	embed.add_field(name="Lookup", value="`.class` [MIL] \n\
Shows the Adventurer class info. \n\
`.ass` [PRIMA] (WIP) \n\
Lists classes. Do `.ass [name]` to lookup a specific class. \n\
`.feat` [MIL] \n\
Lists feats. Do `.feat [name]` to lookup a specific feat. \n\
`.ft` [PRIMA] (WIP) \n\
Lists feats. Do `.ft [name]` to lookup a specific feat. \n\
`.item` [MIL] (WIP) \n\
Lists items. Do `.item [name]` to lookup a specific item. \n\
`.itm` [PRIMA] (WIP) \n\
Lists items. Do `.itm [name]` to lookup a specific item. \n\
`.monster` [MIL] (WIP) \n\
Lists monsters. Do `.monster [name]` to lookup a specific monster. \n\
`.mon` [PRIMA] (WIP) \n\
Lists monsters. Do `.mon [name]` to lookup a specific monster. \n\
`.race` [MIL] (WIP) \n\
Lists races. Do `.race [name]` to lookup a specific race. \n\
`.rce` [PRIMA] (WIP) \n\
Lists races. Do `.rce [name]` to lookup a specific race. \n\
`.spell` [MIL] (WIP) \n\
Lists spells. Do `.spell [name]` to lookup a specific spell. \n\
`.spl` [PRIMA] (WIP) \n\
Lists spells. Do `.spl [name]` to lookup a specific spell.")
	embed.add_field(name="Miscellaneous", value="`.update` {Alias: `.u`}\n\
Forces an update of the Class, Feat, Item, Monster, Race, and Spell databases.")
	embed.add_field(name="For Fun", value="`.echo` \n\
Echoes what you type after `.echo` back to you. Does not delete calling command.")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/348897378062827520/425306674006327307/Compass.png")
	embed.set_footer(text="Lovingly (at times) crafted by Dusk-Argentum#6530.")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True)
async def primaintro(ctx, *, name=""):
	embed=discord.Embed(title="The three of you, while out travelling, recieve a letter from a courier...", color=0x00004c)
	embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/GDzwqMhOw1dGHrnKP5xP7iB7ob44C2j1DoJNC-TOn3c/https/cdn0.iconfinder.com/data/icons/fantasy/512/Fantasy_Scroll.png?width=120&height=120")
	embed.add_field(name="Greetings to you.", value="We have a new mission for you. You are to report to HERO HQ by this Friday, April 13th, at 5 PM, where you will be given further instructions. If you choose to accept it, the reward for this mission is **1000** Gold. We look forward to seeing you.", inline=True)
	embed.add_field(name="Signed,", value="Hero Manager, \
Rudolphus Abelthorn", inline=True)
	embed.set_footer(text="The first session of the PRIMA campaign will take place on Friday, April 13, 2018, at 5 PM EST!")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)

@bot.event
async def on_message(message):
	if message.content.startswith("/shur"):
		await bot.send_message(message.channel, "My dumbfuck programmer (or whoever called this by accident) meant to do the shrug emoji. You know the one. Fucking... ¯\_(ツ)_/¯")
	await bot.process_commands(message)
	
bot.run(TOKEN)
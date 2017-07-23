from discord.ext import commands
import discord.utils
import json, aiohttp
from lxml import etree
from urllib.parse import parse_qs, quote_plus


class No_Owner(commands.CommandError):
    pass


class No_Perms(commands.CommandError):
    pass


class No_Role(commands.CommandError):
    pass


class No_Admin(commands.CommandError):
    pass



class No_Mod(commands.CommandError):
    pass




class No_Sup(commands.CommandError):
    pass


class No_ServerandPerm(commands.CommandError):
    pass


class Nsfw(commands.CommandError):
    pass



owner_id = '203649661611802624'


def is_owner_check(message):
    if message.author.id == owner_id:
        return True
    raise No_Owner()


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))


def embed_perms(message):
    try:
        check = message.author.permissions_in(message.channel).embed_links
    except:
        check = True

    return check


def load_optional_config():
    with open('settings/optional_config.json', 'r') as f:
        return json.load(f)

async def get_google_entries(query):
    params = {
        'q': query,
        'safe': 'off'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
    }
    entries = []
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.google.com/search', params=params, headers=headers) as resp:
            if resp.status != 200:
                config = load_optional_config()
                async with session.get("https://www.googleapis.com/customsearch/v1?q=" + quote_plus(query) + "&start=" + '1' + "&key=" + config['google_api_key'] + "&cx=" + config['custom_search_engine']) as resp:
                    result = json.loads(await resp.text())
                return None, result['items'][0]['link']

            root = etree.fromstring(await resp.text(), etree.HTMLParser())
            search_nodes = root.findall(".//div[@class='g']")
            for node in search_nodes:
                url_node = node.find('.//h3/a')
                if url_node is None:
                    continue
                url = url_node.attrib['href']
                if not url.startswith('/url?'):
                    continue
                url = parse_qs(url[5:])['q'][0]
                entries.append(url)
    return entries, root


def check_permissions(ctx, perms):
    msg = ctx.message
    if is_owner_check(msg):
        return True
    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def role_or_perm(t, ctx, check, **perms):
	if check_permissions(ctx, perms):
		return True
	ch = ctx.message.channel
	author = ctx.message.author
	if ch.is_private:
		return False
	role = discord.utils.find(check, author.roles)
	if role is not None:
		return True
	if t:
		return False
	else:
		raise No_Role()


admin_perms = ['administrator', 'manage_server']
mod_roles = ('mod', 'moderator')
mod_perms = ['manage_messages', 'ban_members', 'kick_members']
def mod_or_perm(**perms):
	def predicate(ctx):
		if ctx.message.channel.is_private:
			return True
		if role_or_perm(True, ctx, lambda r: r.name.lower() in mod_roles, **perms):
			return True
		for role in ctx.message.author.roles:
			role_perms = []
			for s in role.permissions:
				role_perms.append(s)
			for s in role_perms:
				for x in mod_perms:
					if s[0] == x and s[1] == True:
						return True
				for x in admin_perms:
					if s[0] == x and s[1] == True:
						return True
		raise No_Mod()
	return commands.check(predicate)

def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False  # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None

admin_roles = ('admin', 'administrator', 'mod', 'moderator', 'owner', 'god', 'manager', 'boss')
def admin_or_perm(**perms):
	def predicate(ctx):
		if ctx.message.channel.is_private:
			return True
		if role_or_perm(True, ctx, lambda r: r.name.lower() in admin_roles, **perms):
			return True
		for role in ctx.message.author.roles:
			role_perms = []
			for s in role.permissions:
				role_perms.append(s)
			for s in role_perms:
				for x in admin_perms:
					if s[0] == x and s[1] == True:
						return True
		raise No_Admin()
	return commands.check(predicate)


def mod_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name in ('Bot Mod', 'Bot Admin'), **perms)

    return commands.check(predicate)


def admin_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name == 'Bot Admin', **perms)

    return commands.check(predicate)


def is_in_servers(*server_ids):
    def predicate(ctx):
        server = ctx.message.server
        if server is None:
            return False
        return server.id in server_ids
    return commands.check(predicate)


def is_lounge_cpp():
    return is_in_servers('145079846832308224')

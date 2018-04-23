import random
from itertools import zip_longest

import discord
from fuzzywuzzy import process, fuzz


def search(list_to_search: list, key, value, cutoff=5, return_key=False):
    """Fuzzy searches a list for a dict with all keys "key" of value "value"
    result can be either an object or list of objects
    :returns: A two-tuple (result, strict) or None"""
    try:
        result = next(a for a in list_to_search if value.lower() == a.get(key, '').lower())
    except StopIteration:
        result = [a for a in list_to_search if value.lower() in a.get(key, '').lower()]
        if len(result) is 0:
            names = [d[key] for d in list_to_search]
            result = process.extract(value, names, scorer=fuzz.ratio)
            result = [r for r in result if r[1] >= cutoff]
            if len(result) is 0:
                return None
            else:
                if return_key:
                    return [r[0] for r in result], False
                else:
                    return [a for a in list_to_search if a.get(key, '') in [r[0] for r in result]], False
        else:
            if return_key:
                return [r[key] for r in result], False
            else:
                return result, False
    if return_key:
        return result[key], True
    else:
        return result, True


def paginate(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return [i for i in zip_longest(*args, fillvalue=fillvalue) if i is not None]


async def get_selection(ctx, choices, delete=True, return_name=False, pm=False):
    """Returns the selected choice, or None. Choices should be a list of two-tuples of (name, choice).
    If delete is True, will delete the selection message and the response.
    If length of choices is 1, will return the only choice.
    @:raises NoSelectionElements if len(choices) is 0.
    @:raises SelectionCancelled if selection is cancelled."""
    if len(choices) < 2:
        if len(choices):
            return choices[0][1] if not return_name else choices[0]
        else:
            raise Exception("No elements to select from.")
    page = 0
    pages = paginate(choices, 10)
    m = None

    def chk(msg):
        valid = [str(v) for v in range(1, len(choices) + 1)] + ["c", "n", "p"]
        return msg.content.lower() in valid

    for n in range(200):
        _choices = pages[page]
        names = [o[0] for o in _choices if o]
        embed = discord.Embed()
        embed.title = "Multiple Matches Found"
        selectStr = "Which one were you looking for? (Type the number or \"c\" to cancel)\n"
        if len(pages) > 1:
            selectStr += "`n` to go to the next page, or `p` for previous\n"
            embed.set_footer(text=f"Page {page+1}/{len(pages)}")
        for i, r in enumerate(names):
            selectStr += f"**[{i+1+page*10}]** - {r}\n"
        embed.description = selectStr
        embed.colour = random.randint(0, 0xffffff)
        if not pm:
            if n == 0:
                selectMsg = await ctx.bot.send_message(ctx.message.channel, embed=embed)
            else:
                newSelectMsg = await ctx.bot.send_message(ctx.message.channel, embed=embed)
        else:
            embed.add_field(name="Instructions",
                            value="Type your response in the channel you called the command. This message was PMed to you to hide the monster name.")
            if n == 0:
                selectMsg = await ctx.bot.send_message(ctx.message.author, embed=embed)
            else:
                newSelectMsg = await ctx.bot.send_message(ctx.message.author, embed=embed)

        if n > 0:  # clean up old messages
            try:
                await ctx.bot.delete_message(selectMsg)
                await ctx.bot.delete_message(m)
            except:
                pass
            finally:
                selectMsg = newSelectMsg

        m = await ctx.bot.wait_for_message(timeout=30, author=ctx.message.author, channel=ctx.message.channel,
                                           check=chk)
        if m is None:
            break
        if m.content.lower() == 'n':
            if page + 1 < len(pages):
                page += 1
            else:
                await ctx.bot.send_message(ctx.message.channel, "You are already on the last page.")
        elif m.content.lower() == 'p':
            if page - 1 >= 0:
                page -= 1
            else:
                await ctx.bot.send_message(ctx.message.channel, "You are already on the first page.")
        else:
            break

    if delete and not pm:
        try:
            await ctx.bot.delete_message(selectMsg)
            await ctx.bot.delete_message(m)
        except:
            pass
    if m is None or m.content.lower() == "c": raise Exception('Selection timed out or was cancelled.')
    if return_name:
        return choices[int(m.content) - 1]
    return choices[int(m.content) - 1][1]


class EmbedWithAuthor(discord.Embed):
    """An embed with author image and nickname set."""

    def __init__(self, ctx, **kwargs):
        super(EmbedWithAuthor, self).__init__(**kwargs)
        self.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
        self.colour = random.randint(0, 0xffffff)


class LookupException(Exception):
    pass

import hikari
import lightbulb
from datetime import datetime
from lightbulb.ext import tasks

sniper = lightbulb.Plugin("snipe", "snippin yo ass", include_datastore=True)

sniper.d.delsniped = {}
sniper.d.editsniped = {}

@sniper.listener(hikari.GuildMessageDeleteEvent)
async def on_guild_message_delete(event: hikari.GuildMessageDeleteEvent):
    try:
        msg = event.old_message
        if not msg.author.is_bot:
            srvid = msg.guild_id
            chid = msg.channel_id
            auth_name = msg.author.username
            auth_mention = msg.author.mention
            content = msg.content
            try:
                attach = msg.attachments[0]
                attachment_name = attach.filename
                attachment_file = attach.url or attach.proxy_url
            except(IndexError, KeyError):
                attachment_name = None
                attachment_file = None

            # Log Stuff
            # print(f"server:{srvid}, channel:{chid}, author:{auth_name}, content:{content}, url:{attachment_file}") #PRINTS ALL DELETED MESSAGES INTO THE CONSOLE (CAN BE SPAMMY)
            sniper.d.delsniped.update({
                srvid: {
                    chid: {
                        'Author': msg.author,
                        'Sender': auth_name,
                        'Mention': auth_mention,
                        'Content': content,
                        'Attachment': attachment_file,
                        'Filename': attachment_name
                    }
                }
            })
    except:
        pass
        
@sniper.listener(hikari.GuildMessageUpdateEvent)
async def on_guild_message_edit(event: hikari.GuildMessageUpdateEvent):
    try:
        new_msg = event.message
        old_msg = event.old_message
        if not old_msg.author.is_bot:
            srvid = new_msg.guild_id
            chid = new_msg.channel_id
            auth_name = new_msg.author.username
            auth_mention = new_msg.author.mention
            old_message = old_msg.content
            new_message = new_msg.content

            # Log Stuff
            # print(f"server:{srvid}, channel:{chid}, author:{auth_name}, before:{old_message}, after:{new_message}")
            sniper.d.editsniped.update({
                srvid: {
                    chid: {
                        'Author': new_msg.author,
                        'Sender': auth_name,
                        'Mention': auth_mention,
                        'Before': old_message,
                        'After': new_message
                    }
                }
            })
    except:
        pass
        
@sniper.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("snipe", "Allows you to see recently deleted message in the current channel.", aliases=["s","delsnipe"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def deletesnipe(ctx: lightbulb.Context) -> None:
    try:
        author = sniper.d.delsniped[ctx.guild_id][ctx.channel_id]["Author"]
        name = sniper.d.delsniped[ctx.guild_id][ctx.channel_id]["Sender"]
        author_mention = sniper.d.delsniped[ctx.guild_id][ctx.channel_id]["Mention"]
        msg = sniper.d.delsniped[ctx.guild_id][ctx.channel_id]["Content"]
        attachment = sniper.d.delsniped[ctx.guild_id][ctx.channel_id]["Attachment"]
        filename = sniper.d.delsniped[ctx.guild_id][ctx.channel_id]["Filename"]
        
        if isinstance(ctx, lightbulb.PrefixContext):
            await ctx.event.message.delete()
            
        emb = hikari.Embed(description=msg or "Empty Message", timestamp=datetime.now().astimezone())
        emb.set_author(name="Sniped!", icon=author.avatar_url)
        emb.add_field(name="Author:",value=f"{name} ({author_mention})", inline=False)
        emb.set_footer(f"Sniped by: {ctx.author.username}", icon=ctx.author.avatar_url)
        if attachment:
            emb.add_field(name="Attachments",value=f"[{name}]({attachment})")
            if str(filename).endswith(".png") or str(filename).endswith(".gif") or str(name).endswith(".jpg") or str(name).endswith(".jpeg"):
                emb.set_image(attachment)
        await ctx.respond(embed=emb, delete_after=5)
        
    except (KeyError, IndexError):
        await ctx.respond(embed=hikari.Embed(description="⚠ No Message found! Perhaps you're too slow?"), delete_after=3)
    finally:
        del sniper.d.delsniped[ctx.guild_id][ctx.channel_id]

@sniper.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("editsnipe", "Similar to deletesnipe, this command allows you to see edited message.", aliases=["es","esnipe"])
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def editsnipe(ctx: lightbulb.Context) -> None:
    try:
        author = sniper.d.editsniped[ctx.guild_id][ctx.channel_id]["Author"]
        name = sniper.d.editsniped[ctx.guild_id][ctx.channel_id]["Sender"]
        author_mention = sniper.d.editsniped[ctx.guild_id][ctx.channel_id]["Mention"]
        before = sniper.d.editsniped[ctx.guild_id][ctx.channel_id]["Before"]
        after = sniper.d.editsniped[ctx.guild_id][ctx.channel_id]["After"]
        if isinstance(ctx, lightbulb.PrefixContext):
            await ctx.event.message.delete()

        emb = hikari.Embed(timestamp=datetime.now().astimezone())
        emb.set_author(name="Sniped!", icon=author.avatar_url)
        emb.add_field(name="Author:",value=f"{name} ({author_mention})", inline=False)
        emb.add_field(name="Before:", value=before)
        emb.add_field(name="After:", value=after)
        emb.set_footer(f"Sniped by: {ctx.author.username}", icon=ctx.author.avatar_url)
        await ctx.respond(embed=emb, delete_after=5)
    except (KeyError, IndexError):
        await ctx.respond(embed=hikari.Embed(description="⚠ No Message found! Perhaps you're too slow?"), delete_after=3)
    finally:
        del sniper.d.editsniped[ctx.guild_id][ctx.channel_id]

@tasks.task(h=1, auto_start=True)
async def clear_sniper():
    sniper.d.editsniped.clear()
    sniper.d.delsniped.clear()
    

def load(bot) -> None:
    bot.add_plugin(sniper)

def unload(bot) -> None:
    sniper.d.clear()
    bot.remove_plugin(sniper)
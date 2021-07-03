import discord
import time
import asyncio


# requires a folder "/audio" that contains the audio files to be played
# program is coded for just Lorin, Robin and me, with naming convention lorin0.mp3, lorin1.mp3, lorin2.mp3, ....

client = discord.Client()
TOKEN = "" # your token goes here!!!

# show in prompt that bot was successfully connected 
@client.event 
async def on_ready():
    print('Logged in as {0.user}'.format(client))

# sense every message in chats
@client.event
async def on_message(message):

    # do not react to messages send from itself (bot)
    if message.author == client.user:
        return

    # pull up a prompt in chat on how to use the bot
    if message.content == "!help":
        await message.channel.send("Jump into desired channel you want the bot to come into and follow below:\ncommand format: name mp3_number rep_count\nex: lorin 3 4 ..... = play lorin's 3rd spam track 4 times\n\nTo launch an attack on a specific channel, follow the below:\ncommand format: attack discord_tag name mp3_number rep_count\nex: attack 860743034979352586 lorin 1 2 .... = mic spams channel of id:860743034979352586 with lorin 1 2")
        return

    # command format: "name mp3_number rep_count" ex: "lorin 3 4" => play lorin's 3rd spam track 4 times
    mp3_count = [5,5,5] # mp3 counts [lorin, robin, kevin], contains 5 tracks each
    names = ['Lorin', 'Robin', 'Kevin'] # arr for names
    mp3_idx = 0
    rep = 0
    properCmd = 1
    mp3_name_to_play = ""
    channel_id = 0
    atk_flag = 0

    # tokenize message 
    tok_message = message.content.split()
    if tok_message[0] == "attack":
        channel_id = int(tok_message[1])
        atk_flag = 1
        # cut out the attack + channel part for parsing the track name and number of reps
        tok_message[0:2] = tok_message[2:4]
        del tok_message[2:4]
        print(tok_message)
    # construct mp3 person name 
    if tok_message[0] == 'lorin' or tok_message[0] == 'kevin' or tok_message[0] == 'robin':
        mp3_name_to_play = tok_message[0]
        if mp3_name_to_play == "lorin":
            mp3_idx = 0
        elif mp3_name_to_play == "robin":
            mp3_idx = 1
        elif mp3_name_to_play == "kevin":
            mp3_idx = 2
    else:
        properCmd = 0
        await message.channel.send('incorrect command')
    # construct mp3 number 
    if properCmd == 1 and (int(tok_message[1]) >= 1 and int(tok_message[1]) <= mp3_count[mp3_idx]):
        mp3_name_to_play += tok_message[1]
        mp3_name_to_play += ".mp3"
    elif properCmd == 1:
        properCmd = 0
        await message.channel.send('incorrect command')
    # get repitions of attacks  
    if properCmd == 1 and (int(tok_message[2]) <= 10) and (int(tok_message[2]) > 0):
        rep = int(tok_message[2])
    elif properCmd == 1:
        properCmd = 0
        await message.channel.send('incorrect command')


    if properCmd == 1:
        await message.channel.send(names[mp3_idx] + ': HERE I COME EHEHEHEHEHEHEHEHEHE')
        print("playing: ", mp3_name_to_play)
        user = message.author
        if atk_flag == 1:
            # get channel instant from ID
            voice_channel = client.get_channel(channel_id)
            await message.channel.send("Attacking channel: " + str(voice_channel))
            print("Attacking channel: --", voice_channel, "-- of ID:", channel_id)
        else:
            voice_channel = user.voice.channel
        #time.sleep(1)
        if voice_channel!= None:
                while(rep!=0):
                    # connect bot to channel and play music
                    vc = await voice_channel.connect()
                    vc.play(discord.FFmpegPCMAudio("audio/" + mp3_name_to_play), after=lambda e: print('done', e))
                    # sleep on discord side until track finishes playing
                    while vc.is_playing():
                        await asyncio.sleep(1)
                    # stop music 
                    vc.stop()
                    await vc.disconnect()
                    rep -= 1
                    await asyncio.sleep(0.5)
        # don't do anything if voice_channel returns none
        else:
                print('User is not in a channel.')
        
client.run(TOKEN)

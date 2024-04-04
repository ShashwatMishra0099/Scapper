from telethon.sync import TelegramClient
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon import TelegramClient, events
import os

api_id = '29597128'
api_hash = 'feea1340241265662aec5d75678e9573'
bot_token = '7176712779:AAF5HI-iinebKwiE4thcMPR-YuZeam9zgLo'
chat_id = '7176712779'

async def scrape_group(group_name):
    client = TelegramClient('anon', api_id, api_hash)

    await client.start()

    group_entity = await client.get_entity(group_name)

    participants = await client(GetParticipantsRequest(
        group=group_entity,
        filter=ChannelParticipantsSearch('')
    ))

    users = []
    for participant in participants.users:
        user = {
            'id': participant.id,
            'username': participant.username
        }
        users.append(user)

    await client.disconnect()
    
    return users

async def send_message(message):
    async with TelegramClient('anon', api_id, api_hash) as client:
        await client.send_message(chat_id, message)

async def main():
    group_name = os.getenv("TELEGRAM_GROUP_NAME")
    if not group_name:
        print("Error: TELEGRAM_GROUP_NAME environment variable not set.")
        return
    
    users = await scrape_group(group_name)
    scraped_data = "Scraped User Data:\n"
    for user in users:
        scraped_data += f"Username: {user['username']}, User ID: {user['id']}\n"
    
    await send_message(scraped_data)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

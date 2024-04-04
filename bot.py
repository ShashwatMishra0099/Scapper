from telethon.sync import TelegramClient
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest
import json
import sys

api_id = '29597128'
api_hash = 'feea1340241265662aec5d75678e9573'

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

async def main(group_name):
    users = await scrape_group(group_name)
    
    with open('scraped_users.json', 'w') as f:
        json.dump(users, f, indent=4)
    
    print("Scraped User Data:")
    for user in users:
        print(f"Username: {user['username']}, User ID: {user['id']}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python bot.py <group_name>")
        sys.exit(1)
    group_name = sys.argv[1]  # Get group name from command line argument
    import asyncio
    asyncio.run(main(group_name))

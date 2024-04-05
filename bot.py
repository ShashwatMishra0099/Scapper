from telethon.sync import TelegramClient
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest
from fpdf import FPDF
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

def create_pdf(users, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for user in users:
        pdf.cell(200, 10, txt=f"Username: {user['username']}, User ID: {user['id']}", ln=True)
    pdf.output(file_name)

async def send_pdf_via_bot(file_name):
    async with TelegramClient('anon', api_id, api_hash) as client:
        await client.send_file(chat_id, file_name)

async def main():
    async with TelegramClient('anon', api_id, api_hash) as client:
        @client.on(events.NewMessage(pattern='/start', chats=[chat_id]))
        async def start_handler(event):
            # Start the bot functionality when /start command is received
            group_name = input("Enter the name of the public Telegram group: ")
            users = await scrape_group(group_name)
            file_name = f"{group_name}_scraped_users.pdf"
            create_pdf(users, file_name)
            await send_pdf_via_bot(file_name)
            os.remove(file_name)
            print("Scraped user data has been saved as a PDF and sent via Telegram bot.")

        # Run the client event loop
        await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

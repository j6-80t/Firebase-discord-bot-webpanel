import nextcord
from nextcord.ext import commands
import firebase_admin
from firebase_admin import credentials, db
import asyncio

# Firebase 초기화
cred = credentials.Certificate("C:/YOUR_FIREBASE_ADMIN_JSON_FILE")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'YOUR_FIREBASE_PROJECT_DATABASE_URL'
})

intents = nextcord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f'{client.user}ㅣLOGIN')
   
    asyncio.create_task(check_commands())

async def check_commands():
    while True:
        
        ref = db.reference('bot-commands')
        commands_data = ref.get()

        if isinstance(commands_data, dict):  #
            for key, data in commands_data.items():
                if isinstance(data, dict):  
                    command = data.get('command')
                    channel_id = data.get('channelId')

                    if command and channel_id:
                      
                        try:
                            channel_id = int(channel_id)
                        except ValueError:
                            print(f'유효하지 않은 채널 ID: {channel_id}')
                            continue

                        channel = client.get_channel(channel_id) 
                        if channel:
                            if command == 'ping':
                                await channel.send('Pong!')
                            elif command == 'help':
                                await channel.send('도움말')
                            elif command == 'weather':
                              
                                await channel.send('날씨 정보')
                            elif command == 'joke':
                               
                                await channel.send('농담')
                            elif command == 'quote':
                               
                                await channel.send('영감')
                           
                        ref.child(key).delete()
                    else:
                        print(f'데이터 형식 오류: {data}')  
              # 10초
        await asyncio.sleep(10)



client.run('TOKEN')

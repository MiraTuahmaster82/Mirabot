# imports fella
import discord, os, random, threading, dotenv, socket, file, log, json, asyncio, commands
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

class client(discord.Client):
    def __init__(self, *, intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
#start commands fella
    async def setup_hook(self):
        await commands.setup_hook(self)
#end commands fella
    async def on_ready(self):
        print("Signed in as {self.user}")
        
    def stop(self, *args) -> str:
        stopThread = threading.Thread(target=stopBot)
        stopThread.start()
        return "Bot stopped"
    
    def say(self, *args) -> str:
        try:
            if len(args) != 2:
                return "too many or too few arguments, bro"
            channel = asyncio.run_coroutine_threadsafe(
                self.fetch_channel(args[0]),
                self.loop
            ).result()
            asyncio.run_coroutine_threadsafe(
                channel.send(content="\n".join(args[1])),
                self.loop
            ).result()

            return f"bot sayd {args[1]} in {args[0]}"
        except Exception as e:
            log.error(f"Error in say command: {e}")
            return f"failed to send message, {e}"

client = client(intents=intents)

def stopBot():
    os._exit(0)

def handleMessage(message):
    try:
        message = json.loads(message)
        func = message.get("function")
        args = message.get("args", [])

        if hasattr(client, func) and callable(getattr(client, func)):
            return getattr(client, func)(*args)
        else:
            log.warn(f"No {func}")
            return f"Function not found"
    except json.JSONDecodeError:
        return f"Invalid JSON format"
    except Exception as e:
        log.error(f"Error handling message: {e}")
        return f"Error handling message: {e}"

def handleClient(conn):
    with conn:
        data = conn.recv(1024)
        if data:
            response = handleMessage(data.decode())
            log.info(f"Received from terminal: {data.decode()}")
            conn.sendall(response.encode())

def startBotServer():
    try:
        termsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        termsock.bind((settings["IP"], settings["PORT"]))
        termsock.listen(1)
        log.debug("Term <-> Bot Connection open")

        while True:
            conn, _ = termsock.accept()
            log.info("Connection from Terminal")
            termClient = threading.Thread(target=handleClient , args=(conn,))
            termClient.start()
    except socket.error as e:
        log.error(f"Socket error: {e}")
    finally:
        stopBot()

settings = file.Read("Term/settings.json")
severThread = threading.Thread(target=startBotServer)
severThread.start()

client.run(TOKEN)


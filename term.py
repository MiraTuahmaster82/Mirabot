import log, file, socket, json, subprocess

class Term:
    def __init__(self) -> None:
        self.commands = file.Read("Term/commands.json")
        self.settings = file.Read("Term/settings.json")
        self.host = self.settings.get("IP", "localhost")
        self.port = self.settings.get("PORT", 1103) 
        self.lastChannel = ""

        log.info(f"Terminal opened fellow")
        log.debug(f"{self.host} and port {self.port}")

    def botFunction(self, command: str, args:list[str]=[]) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as botSock:
                botSock.connect((self.host, self.port))
                botSock.sendall(json.dumps({
                    "function":f"{command}",
                    "args": args
                }).encode())

                response = botSock.recv(1024)
                log.debug(f"packet from bot: {response.decode()}")
                return response.decode()
        except WindowsError:
            return ''
        except Exception as e:
            log.error(f"Error calling botFunction {command}: {e}")
            return ''

    def handlesubcommands(self, command: str, flags: tuple[str]|list[str]) -> list[str]:
        if isinstance(flags, tuple):
            flags = list(flags)

            matches = []
            for alias in flags:
                for flag in self.commands[command]["flags"]:
                    if alias in flag["alias"]:
                        matches.append(flag["flag"])

            return matches
    
    def execute(self, command: str) -> bool:
        parts = command.split()
        # if command is
        # > test -t -tickle
        commandName = parts[0] # [test]
        flags = parts[1:] # [-t, -tickle]

        for cmd, cmdData in self.commands.items():
            if commandName in cmdData["alias"]:
                funcName = cmdData["call"]
                log.info(f"Terminal called {commandName} with flags {flags}")

                try:
                    func = getattr(self, funcName)
                    func(*flags)
                except Exception as e:
                    log.error(f"failed to call function by command {funcName}: {e}")
                    return False
                break
        else:
            log.warn(f"Command {commandName} not found in commands.json")
            return False
        return True
    
    def main(self) -> None:
        inp = input("> ").strip()
        if inp != "":
            if not self.execute(inp):
                log.error(f"error executing '{inp}'")
            
    def cmdstartbot(self, *flags) -> str:
        log.info("Starting bot")
        call = self.handlesubcommands("start", flags)

        if "debug" in call:
            log.info("Bot started in debug mode")
            subprocess.Popen(["python", "mirabot.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            return "Running bot in debug mode"
        
        log.info("Bot Started in normal mode")
        subprocess.Popen(["pythonw", "mirabot.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        return "Running bot in normal mode"

    def cmdstopbot(self, *flags) -> str:
        log.info("Stopping bot")
        if self.botFunction("stop"):
            log.info("Bot stopped successfully")
            return "Bot stopped successfully"
        return "Bot Not Running or failed to stop"
    
    def cmdbotsay(self, *flags) -> str:
        channel = input("Channel ID: ")
        if channel == "":
            channel = self.lastChannel
        self.lastChannel = channel
        print("bro is whetting they whistle (say something, exit char = >)")
        message = []

        while True:
            line = input("> ").strip()
            if line.lower() == '>':
                break
            if line.lower() == '<':
                print("Canceled")
                return 'Canceled'
            message.append(line)

        if self.botFunction("say", args=[channel, message]):
            return 'Bot Speaking'
        log.warn("Bot not running")
        return 'Bot not running'

    def cmdtest(self, *flags):
        call = self.handlesubcommands("test", flags)

        if "tickle" in call:
            log.error("TICKLE ME FELLOW")
            return 'tickled'



        log.warn("where my tickle at?")
        return 'tested'



def main():
    term = Term()
    
    while True:
        try:
            term.main()
        except Exception as e:
            log.error(e)
            input("")
            break

if __name__ == "__main__":
    main()
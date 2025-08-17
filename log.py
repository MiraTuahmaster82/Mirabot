import datetime, threading

class LogUtils:
	"""This is used as utils for logging stuff, you can use it but its better to call error() or debug()."""
	logFile = "log/latest.txt"
	_lock = threading.Lock()

	# I like getting it fancy
	# returns "Hour:Minute:Second [level] message"
	@staticmethod
	def _format(level:str, message:str) -> str:
		timestamp = datetime.datetime.now().strftime("%H:%M:%S")
		return f"{timestamp} [{level.upper():5}] {message}"

	# This both prints and adds to log, because its *fancy*
	@classmethod
	def _print(cls, level:str, message:str) -> str:
		formatted = cls._format(level, message)

		with cls._lock:
			print(formatted)
			with open(cls.logFile, 'a', encoding='utf-8') as f:
				f.write(formatted+'\n')
		return formatted

# This helps me not copy pasting this a bunch
# There is not really a point to this, but its fine
def _log(level:str, message:str) -> str:
	return LogUtils._print(level, message)


# Other log types can easily be added
# But i dont see a need to

def error(message:str) -> str:
	"""Prints to both console and log."""
	return _log("error", message)

def warn(message:str) -> str:
	"""Prints to both console and log."""
	return _log("warn", message)

def debug(message:str) -> str:
	"""Prints to both console and log."""
	return _log("debug", message)

def info(message:str) -> str:
	"""Prints to both console and log."""
	return _log("info", message)
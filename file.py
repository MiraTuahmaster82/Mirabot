import json, log, os

def exists(file:str) -> bool:
	return os.path.exists(file)

def newJson(file:str) -> 'Read':
	"""
	Create a new JSON file with an empty dictionary if it doesn't exist,
	then return a Read instance to manage it.
	Logs a warning if the file already exists, errors on unexpected issues.
	"""
	folder = os.path.dirname(file)
	if folder and not os.path.exists(folder):
		os.makedirs(folder, exist_ok=True)
	try:
		with open(file, "x", encoding="utf-8") as f:
			json.dump({}, f, indent=4)
	except FileExistsError:
		log.warn(f"File {file} already exists")
		pass
	except Exception as e:
		log.error(f"Unknown error making new file {e}")
	return Read(file)

class Read():
	"""Returns a iterable variable with a path."""

	def __init__(self, file:str):
		self.file = file
		self.data = self.load()

	def load(self):
		"""First inital load of data, do not call unless the data has not been intialized, call reload instead."""
		try:
			with open(self.file, "r", encoding="utf-8") as f:
				return json.load(f)
		except (FileNotFoundError, json.JSONDecodeError) as e:
			raise Exception(f"Failed to read {self.file}: {e}")
	
	def save(self):
		"""Saves back to the file used."""
		try:
			with open(self.file, "w", encoding="utf-8") as f:
				json.dump(self.data, f, indent=4)
			self.reload()
		except Exception as e:
			raise Exception(f"Failed to write {self.file}: {e}")
	
	def reload(self):
		"""Reloads the data stored. Save first or else you will lose info."""
		self.data = self.load()

	def __getitem__(self, key):
		return self.data[key]

	def __setitem__(self, key, value):
		self.data[key] = value

	def __delitem__(self, key):
		del self.data[key]

	def __contains__(self, key):
		return key in self.data

	def __repr__(self):
		return repr(self.data)
	
	def get(self, key, default=None):
		"""Returns a value from (key) unless there is no value else returns (default) or None if not set."""
		return self.data.get(key, default)
	
	def items(self):
		"""Acts the same as Dict.items()"""
		return self.data.items()
	
	def keys(self):
		"""Acts the same as Dict.keys()"""
		return self.data.keys()
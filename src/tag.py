import sys
import csv
import json
import urllib.request

ANKI_CONNECT_URL = "http://127.0.0.1:8765"
LOG_FILE = "MISSING.log"
DECK_NAME = "Chinese"
KEY_NAME = "Hanzi"

def invoke(action, **params):
	req = urllib.request.Request(
		ANKI_CONNECT_URL,
		data=json.dumps({
			"action": action,
			"version": 6,
			"params": params,
		}).encode("utf-8"),
		headers={"Content-Type": "application/json"},
	)

	try:
		with urllib.request.urlopen(req) as resp:
			data = json.load(resp)
	except urllib.error.URLError as e:
		print(f"Error: could not connect to AnkiConnect at {ANKI_CONNECT_URL}: {e}", file=sys.stderr)
		sys.exit(1)
	except json.JSONDecodeError as e:
		print(f"Error: received invalid JSON from AnkiConnect: {e}", file=sys.stderr)
		sys.exit(1)
	except Exception as e:
		print(f"Error: request to AnkiConnect failed: {e}", file=sys.stderr)
		sys.exit(1)

	if data.get("error") is not None:
		print(f"Error: AnkiConnect returned an error for action '{action}': {data['error']}", file=sys.stderr)
		sys.exit(1)

	return data["result"]

def log_a(msg: str):
	print(msg)
	with open(LOG_FILE, "a", encoding="utf-8") as f:
		f.write(msg + "\n")

# Adds tag to exact match
def add_tag_to_exact_match(deck_name: str, key_name: str, key_value: str, tag: str):
	query = f'deck:"{deck_name}" {key_name}:"{key_value}"'
	note_ids = invoke("findNotes", query=query)

	matched = []
	for note in invoke("notesInfo", notes=note_ids) if note_ids else []:
		fields = note["fields"]
		if key_name in fields and fields[key_name]["value"] == key_value:
			matched.append(note["noteId"])

	if not matched:
		log_a(f"Unable to add tag '{tag}' for {key_name}='{key_value}'. No exact match found!")
		return 1

	result = invoke("addTags", notes=matched, tags=tag)
	if result is None:
		print(f"Succesfully added tag '{tag}' to {len(matched)} note(s) with {key_name}='{key_value}'")
		return 0
	else:
		log_a(f"Error adding tag '{tag}' with {key_name}='{key_value}': {result}")
		return 1

# Logic
if len(sys.argv) != 3:
	print("Usage: python tags.py file.csv tag_prefix")
	sys.exit(1)

file = sys.argv[1]
tag_prefix = sys.argv[2]

try:
	with open(file, "r", encoding="utf-8-sig", newline="") as f:
		reader = csv.DictReader(f)
		for row in reader:
			section, simplified = row["section"], row["simplified"]
			full_tag = tag_prefix + "::" + section.capitalize()
			add_tag_to_exact_match(DECK_NAME, KEY_NAME, simplified, full_tag)
except FileNotFoundError:
    print(f"Error: {file} not found")
except PermissionError:
    print("Error: permission denied")
except OSError as e:
    print(f"Error opening file: {e}")

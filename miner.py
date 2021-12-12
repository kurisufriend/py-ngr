from hashlib import sha256
from random import choice
from threading import Thread
import time
_B64SIZE = 76
_ALLCHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
HASHES_CHECKED = 0
HASHES_COLLECTED = 0
HASHES = {}

def hex2nhex(inp):
	inp = inp.lower()
	reps = {"a":"n", "b":"i", "c":"g", "e":"r", "d":"e", "f":"o"}
	for rep in reps:
		inp = inp.replace(rep, reps[rep])
	return inp
def save():
	global HASHES
	while True:
		time.sleep(10)
		if len(HASHES) == 0: continue
		buf = ""
		for h in HASHES:
			buf += ":".join([h, hex2nhex(HASHES[h])])+"\n"
		f = open("NGRwallet", "a")
		f.write(buf)
		f.close()
		HASHES = {}

def progress():
	while True:
		start = HASHES_CHECKED
		time.sleep(10)
		end = HASHES_CHECKED
		print("hashes found:", HASHES_COLLECTED,"\nhashes checked:", HASHES_CHECKED, "\nhashes per second:", (end-start)/10)
def brute():
	global HASHES_CHECKED
	global HASHES_COLLECTED
	while True:
		b64 = ""
		for i in range(0, _B64SIZE):
			b64 += choice(_ALLCHARS)
		hashed = sha256(b64.encode("ascii")).hexdigest()
		HASHES_CHECKED += 1
		if "abccde" in hashed:
			HASHES[b64] = hashed
			HASHES_COLLECTED += 1
def main():
	Thread(target=brute, args=()).start()
	Thread(target=progress, args=()).start()
	Thread(target=save, args=()).start()
if __name__ == "__main__":
	main()
import sys

# English alphabet along with the character frequencies
alpha = "abcdefghijklmnopqrstuvwxyz"
p = [.082,.015,.028,.043,.127,.022,.020,.061,.070,.002,.008,.040,.024,.067,.075,.019,.001,.060,.063,.091,.028,.010,.023,.001,.020,.001]

# Removes all non alphabetic characters and coverts it to lowercase
def filter(string):
	return ''.join([c.lower() for c in string if c.isalpha()])

# Finds the frequencies of all english letters in the given string
def frequency(string):
	freq = {}
	for c in alpha:
		freq[c] = string.count(c)
	return freq

# Friedman test
def test(ciphertext, keylength):
	print(f"Keylength: {keylength}")
	x = filter(ciphertext)
	for i in range(keylength):
		sub = x[i::keylength] # Splits string into every nth character starting from i
		print(indexOfCoincidence(sub))

# Calculates the index of coincidence of a string
def indexOfCoincidence(s):
	freq = frequency(s)
	return sum([freq[l] * (freq[l] - 1) for l in freq])/(len(s) * (len(s) - 1))

# Generates the table and tries to guess a possible key
def analyze(ciphertext, keylength):
	x = filter(ciphertext)
	header = "g  |" + '|'.join([f"    m{i}    " for i in range(keylength)])
	print(header + "\n" + "-" * len(header))
	sub = [frequency(x[i::keylength]) for i in range(keylength)]
	sub = [[elem[v] for v in elem] for elem in sub]
	maximum = [0] * keylength
	key = [''] * keylength
	for g in range(26):
		results = []
		for v in sub:
			v_shift = v[g:] + v[0:g]
			results.append(sum([p[i] * v_shift[i] for i in range(len(p))]))
		for i in range(len(results)):
			if maximum[i] < results[i]:
				maximum[i] = results[i]
				key[i] = alpha[g]
		print("%2d |" % g, end='')
		print('|'.join(["  %6.2f  " % res for res in results]))
	print(f"Possible key: {''.join(key)}")

# Decodes vigenere cipher given the keyword
def decode(x, keyword):
	plaintext = ""
	keyword = keyword.lower()
	keylength = len(keyword)
	c = 0
	for i in range(len(x)):
		if x[i].isalpha():
			value = (ord(x[i].lower()) - ord(keyword[c % keylength])) % 26
			c += 1
			plaintext += chr(value + 65) # to convert back to ASCII printable
		else:
			plaintext += x[i]
	print(plaintext)


# Command line argument parsing
try:
	f = open(sys.argv[3], 'r')
	ciphertext = f.read().strip()
	if sys.argv[1] == "test":
		test(ciphertext, int(sys.argv[2]))
	elif sys.argv[1] == "analyze":
		analyze(ciphertext, int(sys.argv[2]))
	elif sys.argv[1] == "decode":
		decode(ciphertext, sys.argv[2])
	else:
		raise Exception
except Exception as e:
	print("Usage: vigenere.py test|analyze|decode keylength|keyword ciphertext-filename")
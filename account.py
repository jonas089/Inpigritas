import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # RSA algorithm to sign with priv & verify with pub
from Crypto.Hash import SHA384
import hashlib
import time
import values
import pickle

class Keys:

	# Generates Keypair And Saves Both PRIVATE and PUBLIC KEY to your LOCAL Drive
	def Generate_Keypair(passwd=None): # added functionality for password protection (private key), will make default in the future
		key = RSA.generate(2048)
		try:
			os.mkdir('keys/')
		except Exception as exists:
			pass
		try:
			open('keys/private_key.pem', 'x')
		except Exception as exists:
			pass
		try:
			open('keys/public_key.pem', 'x')
		except Exception as exists:
			pass

		with open('keys/private_key.pem', 'wb') as private_key_file:
			private_key_file.write(key.exportKey('PEM', passphrase=passwd))
			private_key_file.close()
		with open('keys/public_key.pem', 'wb') as public_key_file:
			public_key_file.write(key.publickey().exportKey('PEM'))
			public_key_file.close()

	def Export_Pubkey():
		with open('keys/public_key.pem', 'r') as public_key_file:
			pubkey_pem = public_key_file.read()#pubkey.exportKey('PEM')
			return pubkey_pem

	def Import_Pubkey():
		with open('keys/public_key.pem', 'r') as public_key_file:
			pubkey = RSA.importKey(public_key_file.read())
			return pubkey

	def Import_Privkey(passwd=None): # added functionality for password protection (private key), will make default in the future
		with open('keys/private_key.pem', 'r') as private_key_file:
			privkey = RSA.importKey(private_key_file.read(), passphrase=passwd)
			return privkey

	def Generate_Address():
		publickey = Keys.Import_Pubkey()
		Address_data_string = str(publickey)
		sha = hashlib.sha384()
		Address_hash = sha.update(Address_data_string.encode('utf-8'))
		Address_hash_hex = sha.hexdigest()
		Address = str(Address_hash_hex)
		return Address
		# Address is a hash representation of the string of the publickey => this ensures nobody can create a fake transaction by
		# using somebody else's Address combined with his own publickey => if Address != pubkey hashed : return False

def LoadBalance(address):
	Balance = 0.0
	with open('src/blockchain.dat', 'rb') as ChainFile:
		LocalBlockChain = pickle.load(ChainFile)

	for Block in range(0, len(LocalBlockChain)):
		for Transaction in range(0, len(LocalBlockChain[Block]['transactions'])):
			if LocalBlockChain[Block]['transactions'][Transaction]['sender'] == address:
				Balance -= LocalBlockChain[Block]['transactions'][Transaction]['amount']
			if LocalBlockChain[Block]['transactions'][Transaction]['recipient'] == address:
				Balance += LocalBlockChain[Block]['transactions'][Transaction]['amount']
	#	with open('src/TxBlockNo' + '000' + str(Block) + '.dat', 'rb') as Block_Transactions_File:
	#		block_transaction_data = pickle.load(Block_Transactions_File)
	#		for tx in range(0, len(block_transaction_data) - 1):
	#			if block_transaction_data[tx]['sender'] == address:
	#				Balance -= block_transaction_data[tx]['amount']
	#			if block_transaction_data[tx]['recipient'] == address:
	#				Balance += block_transaction_data[tx]['amount']

	# calculate interest
	Interest = 0.0
	block_balance = 0.0
	for Block_In_Chain in range(0, len(LocalBlockChain)):
		for TxInBlock in range (0, len(LocalBlockChain[Block_In_Chain]['transactions'])):
			if LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['sender'] == address:
				block_balance -= LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['amount']
			elif LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['recipient'] == address:
				block_balance += LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['amount']
			elif LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['recipient'] == address and LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['sender'] == address:
				block_balance += 0.0
			else:
				last_balance_to_proceed = 0.0
				for Block in range(0, TxInBlock):
					for Transaction in range(0, len(LocalBlockChain[Block]['transactions'])):
						if LocalBlockChain[Block]['transactions'][Transaction]['sender'] == address:
							last_balance_to_proceed -= LocalBlockChain[Block]['transactions'][Transaction]['amount']
						if LocalBlockChain[Block]['transactions'][Transaction]['recipient'] == address:
							last_balance_to_proceed += LocalBlockChain[Block]['transactions'][Transaction]['amount']
				block_balance = last_balance_to_proceed				
		if block_balance > 0.0:
			Interest += block_balance * values.interest_per_block
	Balance += Interest

	next_index = LocalBlockChain[len(LocalBlockChain) - 1]['index'] + 1

	try:
		with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'rb') as Block_Transaction_File:
			Block_Transactions_Unconfirmed = pickle.load(Block_Transaction_File)
		for uftx in range(0, len(Block_Transactions_Unconfirmed) - 1):
			if Block_Transactions_Unconfirmed[uftx]['sender'] == sender:
				Balance -= Block_Transactions_Unconfirmed[uftx]['amount']
			if Block_Transactions_Unconfirmed[uftx]['recipient'] == sender:
				Balance += Block_Transactions_Unconfirmed[utfx]['amount']
	except Exception as notransactions:
		print('[WARNING] NO TRANSACTION FILE FOUND FOR FOLLOWING BLOCK')
	return Balance



def __Start__():
	new_wallet = False
	try:
		open('keys/private_key.pem', 'x')
		new_wallet = True
	except Exception as exists:
		pass
	try:
		open('keys/public_key.pem', 'x')
		new_wallet = True
	except Exception as exists:
		pass
	if new_wallet == True:
		Keys.Generate_Keypair()
		Addresses = []
		Addresses.append(0)
		Addresses[0] = str(Keys.Generate_Address())
		print('[NEW ADDRESS]' + Addresses[0])
		open('keys/account.dat', 'x')
		with open('keys/account.dat', 'wb') as account_file:
			pickle.dump(Addresses, account_file)
	else:
		return




#[NOTES]
#			[SAMPLE FOR KEYS AND SIGNATURE]
#			with open('keys/public_key.pem' , 'r') as public_key_file:
#				public_key = RSA.importKey(public_key_file.read())
#				self.pubkey = public_key.exportKey('PEM')



#				hash_utf = self.hash.encode('utf-8')
#				with open('keys/private_key.pem', 'r') as privkey_File:
#					privkey = RSA.importKey(privkey_File.read())
#				genSHA = SHA256.new()
#				genSHA.update(hash_utf)
#				self.sigf = genSHA
#				unique_cipher = PKCS1_v1_5.new(privkey)
#				# genSHA=sigf
#				self.sig = unique_cipher.sign(genSHA)


#		genSHA = SHA256.new()
#		genSHA.update(blockhash.encode('utf-8'))
#		cypher = PKCS1_v1_5.new(pubkey)
#		verification = cypher.verify(genSHA, sig)
#		assert verification, print('Error in Block verification')#return False

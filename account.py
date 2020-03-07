import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # RSA algorithm to sign with priv & verify with pub
from Crypto.Hash import SHA384
import hashlib

import pickle

class Keys:

	# Generates Keypair And Saves Both PRIVATE and PUBLIC KEY to your LOCAL Drive
	def Generate_Keypair():
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
			private_key_file.write(key.exportKey('PEM'))
			private_key_file.close()
		with open('keys/public_key.pem', 'wb') as public_key_file:
			public_key_file.write(key.publickey().exportKey('PEM'))
			public_key_file.close()

	def Export_Pubkey():
		with open('keys/public_key.pem', 'r') as public_key_file:
			pubkey_string_rep = public_key_file.read()
			return pubkey_string_rep

	def Import_Pubkey():
		with open('keys/public_key.pem', 'r') as public_key_file:
			pubkey = RSA.importKey(public_key_file.read())
			return pubkey

	def Import_Privkey():
		with open('keys/private_key.pem', 'r') as private_key_file:
			privkey = RSA.importKey(private_key_file.read())
			return privkey

	def Generate_Address():
		publickey = Keys.Import_Pubkey()
		privatekey = Keys.Import_Privkey()
		sigvar = SHA384.new()
		sigvar.update(str(publickey).encode('utf-8'))
		address_cipher = PKCS1_v1_5.new(privatekey)
		Address = address_cipher.sign(sigvar)
		return Address

#[TESTING]
def Validate_Address(Export_Publickey, ByteArray_Address):
	publickey = RSA.importKey(Export_Publickey)
	sigvar = SHA384.new()
	sigvar.update(str(publickey).encode('utf-8'))
	cypher = PKCS1_v1_5.new(publickey)
	verification = cypher.verify(sigvar, ByteArray_Address)
	return verification






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
		Addresses[0] = Keys.Generate_Address()
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
#Inpigritas - a blockchain based transaction system in python, by Jonas Pauli
Co-author: Carl Romedius Speck

## Introduction
Inpigritas is the prototype of a digital transaction network developed in Python.
The nodes operate similar to a REST api and a Python-Flask webserver serves the routes. This setup is not ideal, considering the low transaction speeds, however allowed for an efficient proof of concept. Inpigritas is described as a "blockchain based transaction network", rather than a cryptocurrency, as I have not yet implemented a consens algorithm / there is no mechanism for decentralized distribution of a currency or a token. I see this project as a proof of concept, as Inpigritas demonstrates an energy efficient, potentially decentralized Network, that could be further developed to become a Fintech application.
I describe Inpigritas as "potentially decentralized", because any IP address can be added to the configuration file and serve as a Node. Similar setup and config files can be found in many outdated cryptocurrency source codes. Inpigritas, especially this Flask-version of Inpigritas is far from a production application and was purely developed out of enjoyment and interest. It was very educational to build this application from scratch, using Flask, pycryptodome library and RSA signatures for message authentication. 
Inpigritas nodes only accept valid blocks. The parameters in a block, aswell as it's blockhash are predefined in the pervious block 
( starting from the Genesis Block, that needs to be in the src folder ). There is no consens between nodes, as every node follows it's local consens. Corrupted nodes can't submit falsified data to legit nodes, as every node stores a full track record of every transaction ( starting from the transaction data hashed in the Genesis block ). The entire supply is (as of now) distributed through the Genesis block. 

## About the Developer
I am a 21 year old software and crypto enthusiast from Germany, living in Switzerland and hoping to become a Fintech developer in a few years. I have been into the cryptocurrency industry since 2015 and started coding in 2016, but I know that I have a long way to go and that I am not yet capable of developing production applications on my own.

If you ( for whatever reason ) wish to try setting up an Inpigritas network on your device, the following guide should ( given you have some experience in IT ) provide you with all the necessary information to do so. 

## Simply setup your local Testnet for Inpigritas and submit transactions to your local Network:
- assuming 2 nodes with empty "src" and "keys" folder(s)

# DEVELOPMENT BUILD
## V.0.0.0

## Step 1:
 # In values.py
   Node#1
   port = 5000
   seeds = ['127.0.0.1:5001']

   Node#2
   port = 5001
   seeds = ['127.0.0.1:5000']
## Step 2:
   cd Node1
   py debugcli.py --newacc
   --> outputs account address ( referenced below as "Node1_Address")

   cd Node2
   py debugcli.py --newacc
   --> outputs account address
## Step 3:
 # In values.py
   dev_address = Node1_Address (see Readme.md line 21)
## Step 4:
 # In validation.py
 [THIS IS EXTREMELY IMPORTANT]
 [DO THIS ONLY FOR NODE 1 !]
   put a hashtag "#" in front of every line of code that is marked as "comment out when generating the genesis block"
## Step 5:
  cd Node1
  py debugcli.py --generategenesis
  --> outputs genesisblock data
## Step 6:
   copy-paste "src" folder from Node1 to Node2
   Revert Step 4 and remove all hashtags placed in that step
   replace "static" variables "genesis_hash" and "genesis_next_hash" with those who were output of Step 5
## Step 7:
   cd into Node 1 and execute:
   py node.py

   cd into Node 2 and execute:
   py node.py

   open a 3rd terminal and cd into Node 1 (premine located),
   then execute a transaction through debugclient as follows:
   py debugcli.py
   # INPUT
   --> amount
   --> recipient

   cd into Node 2 and execute:
   py node.py

   open a 3rd terminal and cd into Node 1 (premine located),
   then execute a transaction through debugclient as follows:
   py debugcli.py --transaction
   # INPUT
   --> amount
   --> recipient

TESTING ENVIRONMENT SETUP SUCCESSFUL IF TRANSACTION ACCEPTED BY NETWORK

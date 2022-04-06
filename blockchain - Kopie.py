import hashlib
from re import T
import string
import time
from msilib.schema import SelfReg
import random

#from sys import last_traceback


class Block():
    def __init__(self, data, previous_hash, index, proof_number, timestamp=None):
        self.nonce = -1
        self.previous_hash = previous_hash
        self.proof_number = proof_number
        self.index = index
        self.data = data
        difficulty = 2
        self.timestamp = timestamp or time.time()
        self.hash = self.compute_hash()
        self.hash = self.mine(difficulty)

    def compute_hash(self):
        string_block = "{}{}{}{}{}".format(self.nonce, self.index, self.proof_number, self.previous_hash, self.data, self.timestamp)
        return hashlib.sha256(str(string_block).encode('utf-8')).hexdigest()
    
    #found
    
    def mine(self, difficulty):
        found = False
        while not found:
            #print(str(self.nonce) + "  "+ str(self.hash))
            self.nonce += 1
            self.hash = self.compute_hash()
            if self.hash[0:difficulty] == "0" * difficulty:
                found = True
                print("Block mined: {}".format(self.hash))
                return self.hash
    
    #validate block
    def validate(self, previous_hash):
        if self.previous_hash != previous_hash:
            return False
        if self.hash != self.compute_hash():
            return False
        return True


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.data = []
        self.wallets = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        self.data = "This is the Genesis Block Data"
        genesisblock = Block(self.data,0000000000000000000000000000000000000000000000000000000000000000,0, 0, time.time())
        self.chain.append(genesisblock)

    def addBlock(self, data):
        time.sleep(0.1)
        block = Block(data, self.chain[-1].hash, len(self.chain), time.time())
        self.chain.append(block)

    def returnHashAndIndex(self):
        #funtion to print details of the block
        for i in range(len(self.chain)):
            print("Block Hash: ", self.chain[i].hash)
            print("Block Index: ", self.chain[i].index)
            print("Block Proof Number: ", self.chain[i].proof_number)
            print("Block Timestamp: ", self.chain[i].timestamp)
            print("\n")
        
    #function to validate the block
    def validateBlockWithPrevious(self, block):
        previous_block = self.chain[block.index - 1]
        if previous_block.index + 1 != block.index:
            print("Block index not valid i")
            return False
        elif block.timestamp <= previous_block.timestamp:
            print("Block index not valid t")
            return False
        else:
            print("Block index valid")
            return True

    #function to create wallet
    
    def createWallet(self):
        
        #create a wallet
        wallet = {}
        #create a private key
        wallet['private_key'] = self.generatePrivateKey()
        #create a public key
        wallet['public_key'] = self.generatePublicKey(wallet['private_key'])
        #create a public address
        wallet['public_address'] = self.generatePublicAdress(wallet['public_key'])
        #create a balance
        wallet['balance'] = 0
        #creat a list of transactions
        #print all
        print("\n")
        print("Wallet Created:")
        print("Private Key:     ", wallet['private_key'])
        print("Public Key:      ", wallet['public_key'])
        print("Public Address:  ", wallet['public_address'])

        self.wallets.append(wallet)
        return wallet
    
    def generatePrivateKey(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
    def generatePublicKey(self, private_key):
        return hashlib.sha256(str(private_key).encode('utf-8')).hexdigest()
    def generatePublicAdress(self, public_key):
        return hashlib.sha256(str(public_key).encode('utf-8')).hexdigest()
    
    #function transaction
    def transaction(self, transaction):
        if not self.verifyTransaction(transaction):
            return False
        sender_wallet = transaction['sender_wallet']
        sender_wallet['balance'] -= transaction['amount']
        self.data.append(transaction)
        return True

    #verify transaction
    def verifyTransaction(self, transaction):
        #public_key = self.wallets[transaction['sender_wallet']]['public_key']
        public_key = self.wallets[0]['public_key']
        signature = transaction['signature']
        string_transaction = "{}{}{}".format(transaction['recipient_address'], transaction['amount'], transaction['timestamp'])
        return self.verifySignature(public_key, signature, string_transaction)

    #function with wallet to create transaction
    def createTransaction(self, sender_wallet, recipient_address, amount):
        transaction = {
            'sender_wallet': sender_wallet,
            'recipient_address': recipient_address,
            'amount': amount,
            'timestamp': time.time()
        }
        return transaction
    
    #function to sign transaction
    def signTransaction(self, transaction, sender_private_key):
        transaction['signature'] = self.generateSignature(transaction, sender_private_key)
        return transaction

    #function to generate signature
    def generateSignature(self, transaction, sender_private_key):
        string_transaction = "{}{}{}".format(transaction['recipient_address'], transaction['amount'], transaction['timestamp'])
        return hashlib.sha256(str(string_transaction).encode('utf-8')).hexdigest()
    


blockchain = BlockChain()
blockchain.addBlock("Person 1 20CHF-> Person 2")
blockchain.addBlock("Person 2 20CHF-> Person 3")
blockchain.addBlock("Person 3 20CHF-> Person 4")
blockchain.addBlock("Person 4 20CHF-> Person 5")
#print validate block


#blockchain.validateBlock(blockchain.chain[3])
##blockchain.returnHashAndIndex()
#change hash of chain 1 to 74382748349
#blockchain.chain[1].hash = "74382748349"
#blockchain.chain[2].index = 45

#blockchain.validateBlockWithPrevious(blockchain.chain[4])
#blockchain.generatePrivateKey()

blockchain.createWallet()
blockchain.createWallet()

#print(blockchain.chain[1].mine(2))
#print(blockchain.chain[1].validate(blockchain.chain[0].hash))
#print(blockchain.wallets[0]['public_address'])
#print(blockchain.wallet)
#print wallet 1

blockchain.wallets[0]['balance'] = 20
print(blockchain.wallets[1]['balance'])
transaction2 = blockchain.createTransaction(blockchain.wallets[0], blockchain.wallets[1]['public_address'], 20)
#blockchain.signTransaction(transaction2, blockchain.wallets[0]['private_key'])
blockchain.verifyTransaction(transaction2)
blockchain.Transaction(transaction2)

print("ENDE")
print(blockchain.wallets[1]['balance'])
#print trancation
#print(transaction2)
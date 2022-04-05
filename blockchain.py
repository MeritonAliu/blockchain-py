import hashlib
import string
import time
from msilib.schema import SelfReg


class Block():
    def __init__(self, data, previous_hash, index, proof_number, timestamp=None):
        self.hash = hashlib.sha256(str(data).encode('utf-8')).hexdigest()
        self.previous_hash = previous_hash
        self.proof_number = proof_number
        self.index = index
        self.data = data
        self.timestamp = timestamp or time.time()

class BlockChain():
    def __init__(self):
        self.chain = []
        self.createGenesisBlock("This is the Genesis Block Data")
    def createGenesisBlock(self,data):
        genesisblock = Block(data,0000000000000000000000000000000000000000000000000000000000000000,0, 0, time.time())
        self.chain.append(genesisblock)
        print(genesisblock.timestamp)
    def addBlock(self, data):
        block = Block(data, self.chain[-1].hash, len(self.chain), 3, time.time())
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
    def validateBlock(self, block, previous_hash):
        """"
        if previous_block.index + 1 != block.index:
        print("Block is not valid")
        return False

        elif previous_block.compute_hash() != block.previous_hash:
            print("Block is not valid")
            return False

        elif block.timestamp & lt; = previous_block.timestamp:
            print("Block is not valid")
            return False

        print("Block is valid")
        return True
        """
        pass
        
       

blockchain = BlockChain()
blockchain.addBlock("Person 1 20CHF-> Person 2")
blockchain.addBlock("Person 1 20CHF-> Person 2")
blockchain.addBlock("Person 2 20CHF-> Person 3")
blockchain.addBlock("Person 3 20CHF-> Person 4")
blockchain.addBlock("Person 4 20CHF-> Person 5")
blockchain.addBlock("Person 5 20CHF-> Person 6 ")
#blockchain.validateBlock(blockchain.chain[3])
blockchain.returnHashAndIndex()



import hashlib
import time

class Block:
    def __init__(self, index, proof_no, prev_hash, data, timestamp):
        self.index = index
        self.proof_no = proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp

    def generate_hash(self):
        
        hash = hashlib.sha256(bytes(f'{self.index}{self.proof_no}{self.prev_hash}{self.data}{self.timestamp}', 'utf-8')).hexdigest()
        return hash

    def __repr__(self):
        
        return f'''
        Index : {self.index}
        Proof Number : {self.proof_no}
        Previous Hash : {self.prev_hash}
        Data : {self.data}
        Timestamp : {self.timestamp}
        '''


class BlockChain:
    def __init__(self):
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.construct_genesis()

    def construct_genesis(self):
        self.construct_block(proof_no=0, prev_hash=0)

    def construct_block(self, proof_no, prev_hash):
        block = Block(
            index = len(self.chain),
            proof_no=proof_no,
            prev_hash=prev_hash,
            data = self.current_data,
            timestamp = time.time()
            )
        self.chain.append(block)
        self.current_data = []
        return block

    @staticmethod
    def check_validity(block , prev_block):
        if block.index - 1 != prev_block.index:
            return False
        elif prev_block.generate_hash != block.prev_hash :
            return False
        elif prev_block.timestamp >= block.timestamp :
            return False
        elif not verify_proof(block.proof_no, prev_block.proof_no):
            return False
        return True

    def add_data(self, sender, reciever, quantity):
        self.current_data.append({
            'sender' : sender,
            'reciever' : reciever,
            'quantity' : quantity
        })
        return True

    @staticmethod
    def add_proof(last_proof):
        proof_no = 0
        while not BlockChain.verify_proof(last_proof, proof_no):
            print(proof_no)
            proof_no += 1

        return proof_no

    @staticmethod
    def verify_proof(last_proof, proof_no):
        guess_hash = hashlib.sha256(bytes(f'{last_proof}{proof_no}', 'utf-8')).hexdigest()
        print(guess_hash)
        return guess_hash[:8] == '0000'

    @property
    def last_block(self):
        return self.chain[-1]

    def mine(self, miner_details):
        self.add_data(
            sender = '0',
            reciever = miner_details,
            quantity = 1
        )

        last_block = self.last_block

        last_proof = last_block.proof_no
        proof = self.add_proof(last_proof)
        hash = last_block.generate_hash()

        block = self.construct_block(proof_no=proof, prev_hash=hash)
        return vars(block)

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def obtain_block_object(block_data):
        return Block(
            block_data['index'],
            block_data['proof_no'],
            block_data['prev_hash'],
            block_data['data'],
            block_data['timestamp']
        )



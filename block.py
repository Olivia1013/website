import hashlib
import time
import json

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0, difficulty=0, mining_time=0.0, mining_speed=0.0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.difficulty = difficulty
        self.mining_time = mining_time
        self.mining_speed = mining_speed
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        self.difficulty = difficulty
        target = "0" * difficulty
        start = time.time()
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        self.mining_time = time.time() - start
        self.mining_speed = self.nonce / self.mining_time if self.mining_time > 0 else 0.0
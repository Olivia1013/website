from block import Block
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4  # 可以调整难度
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # 检查当前区块的哈希是否正确
            if current_block.hash != current_block.calculate_hash():
                return False

            # 检查前一个区块的哈希是否匹配
            if current_block.previous_hash != previous_block.hash:
                return False

        return True
from block import Block
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4  # 可以调整难度
        self.history = []  # 历史统计，用于图表展示
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self._record_history(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self._record_history(new_block)
        return {
            'mining_time': round(new_block.mining_time, 3),
            'nonce': new_block.nonce,
            'mining_speed': round(new_block.mining_speed, 3),
            'difficulty': new_block.difficulty
        }

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

    def tamper_block(self, index, new_data):
        if 0 < index < len(self.chain):
            block = self.chain[index]
            block.data = new_data
            block.hash = block.calculate_hash()
            return True
        return False

    def _record_history(self, block):
        note = '创世区块作为链的起点。'
        if block.index > 0:
            note = f'区块#{block.index}完成挖矿，耗时 {block.mining_time:.3f} 秒，挖矿速度约 {block.mining_speed:.2f} Nonce/秒。'

        self.history.append({
            'timestamp': time.time(),
            'block_index': block.index,
            'block_timestamp': block.timestamp,
            'chain_length': len(self.chain),
            'difficulty': self.difficulty,
            'mining_time': round(block.mining_time, 3),
            'nonce': block.nonce,
            'mining_speed': round(block.mining_speed, 3),
            'note': note
        })

    def _record_difficulty_change(self):
        """记录难度变化到历史"""
        self.history.append({
            'timestamp': time.time(),
            'chain_length': len(self.chain),
            'difficulty': self.difficulty,
            'mining_time': 0,
            'nonce': 0,
            'mining_speed': 0
        })

    def get_history(self):
        return self.history

    def set_difficulty(self, difficulty):
        if isinstance(difficulty, int) and difficulty >= 1:
            self.difficulty = difficulty
            self._record_difficulty_change()  # 记录难度变化
            return True
        return False
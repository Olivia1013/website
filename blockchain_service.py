from queue import Queue
from threading import Lock
from blockchain import Blockchain
from block import Block
import json

class BlockchainService:
    def __init__(self):
        self.blockchain = Blockchain()
        self.listeners = []
        self.listeners_lock = Lock()

    def get_state(self):
        return {
            'chain': [self._block_to_dict(b) for b in self.blockchain.chain],
            'valid': self.blockchain.is_chain_valid(),
            'difficulty': self.blockchain.difficulty,
            'history': self.blockchain.get_history()
        }

    def add_block(self, data):
        block = Block(len(self.blockchain.chain), __import__('time').time(), data, '')
        result = self.blockchain.add_block(block)
        self._notify_all({
            'type': 'chain_update',
            'chain': [self._block_to_dict(b) for b in self.blockchain.chain],
            'valid': self.blockchain.is_chain_valid(),
            'stats': self.blockchain.get_history(),
            'detail': result
        })
        return result

    def tamper_block(self, index, new_data):
        success = self.blockchain.tamper_block(index, new_data)
        self._notify_all({
            'type': 'tamper',
            'chain': [self._block_to_dict(b) for b in self.blockchain.chain],
            'valid': self.blockchain.is_chain_valid(),
            'stats': self.blockchain.get_history(),
            'tampered_index': index,
            'success': success
        })
        return success

    def validate(self):
        valid = self.blockchain.is_chain_valid()
        return valid

    def set_difficulty(self, difficulty):
        ok = self.blockchain.set_difficulty(difficulty)
        if ok:
            self._notify_all({
                'type': 'difficulty_update',
                'difficulty': self.blockchain.difficulty,
            })
        return ok

    def attach_listener(self):
        q = Queue()
        with self.listeners_lock:
            self.listeners.append(q)
        return q

    def detach_listener(self, q):
        with self.listeners_lock:
            if q in self.listeners:
                self.listeners.remove(q)

    def _notify_all(self, message):
        text = json.dumps(message)
        with self.listeners_lock:
            for q in list(self.listeners):
                q.put(text)

    def _block_to_dict(self, block):
        return {
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'nonce': block.nonce
        }

service = BlockchainService()
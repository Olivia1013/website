from blockchain import Blockchain
from block import Block
import time

def main():
    # 创建区块链实例
    blockchain = Blockchain()

    print("创世区块已创建。")
    print(f"创世区块哈希: {blockchain.chain[0].hash}")

    # 添加新区块
    print("\n添加新区块...")
    block1 = Block(1, time.time(), "交易数据1", "")
    blockchain.add_block(block1)

    block2 = Block(2, time.time(), "交易数据2", "")
    blockchain.add_block(block2)

    # 打印区块链
    print("\n区块链内容:")
    for block in blockchain.chain:
        print(f"区块 {block.index}:")
        print(f"  时间戳: {block.timestamp}")
        print(f"  数据: {block.data}")
        print(f"  前哈希: {block.previous_hash}")
        print(f"  哈希: {block.hash}")
        print(f"  Nonce: {block.nonce}")
        print()

    # 验证区块链
    print("验证区块链完整性:")
    print(f"链有效: {blockchain.is_chain_valid()}")

    # 尝试篡改区块链
    print("\n尝试篡改区块1的数据...")
    blockchain.chain[1].data = "篡改的数据"
    blockchain.chain[1].hash = blockchain.chain[1].calculate_hash()  # 重新计算哈希

    print("验证区块链完整性（篡改后）:")
    print(f"链有效: {blockchain.is_chain_valid()}")

if __name__ == "__main__":
    main()
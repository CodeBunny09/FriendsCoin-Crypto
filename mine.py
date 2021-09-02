from blockchain import Block, BlockChain

blockchain = BlockChain()
print("Mining FriendsCoin is about to start!!!")
n = 0
while n <= 1 :
    n += 1
    print(f'Mining {n}th coin....')
    blockchain.mine('Pratik')

print("Mining Successful!!")
print(blockchain.chain)
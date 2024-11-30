from blockchain import Blockchain
from network import Network
from consensus import Consensus

class Node:
    def __init__(self, address):
        self.address = address
        self.blockchain = Blockchain()
        self.network = Network()
        self.consensus = Consensus(self.blockchain)

    def add_transaction(self, transaction):
        self.blockchain.add_transaction(transaction)

    def mine(self):
        self.blockchain.mine_pending_transactions(self.address)
        self.broadcast_chain()

    def broadcast_chain(self):
        self.network.broadcast("chain_update", self.blockchain.chain)

    def resolve_conflicts(self):
        other_chains = self.network.get_chains()
        self.consensus.resolve_conflicts(other_chains)

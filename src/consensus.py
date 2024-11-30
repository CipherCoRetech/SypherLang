from blockchain import Blockchain

class Consensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def resolve_conflicts(self, node_chains):
        longest_chain = self.blockchain.chain
        max_length = len(longest_chain)

        for chain in node_chains:
            if len(chain) > max_length and self.is_chain_valid(chain):
                longest_chain = chain
                max_length = len(chain)

        if longest_chain != self.blockchain.chain:
            self.blockchain.chain = longest_chain
            return True

        return False

    def is_chain_valid(self, chain):
        blockchain = Blockchain()
        blockchain.chain = chain
        return blockchain.is_chain_valid()

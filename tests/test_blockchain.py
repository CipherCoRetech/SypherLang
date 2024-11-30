import unittest
from blockchain import Blockchain
from transaction import Transaction
from node import Node
from network import Network
from consensus import Consensus
import time


class TestBlockchain(unittest.TestCase):
    """
    Test Suite for SypherCore Blockchain Functionality
    This suite tests the functionalities of the blockchain, including transactions, blocks, and nodes.
    """

    def setUp(self):
        """
        Set up the blockchain, network, and nodes for testing.
        """
        # Initialize Blockchain and Node Setup
        self.blockchain = Blockchain()
        self.node1 = Node('Node_1', self.blockchain)
        self.node2 = Node('Node_2', self.blockchain)

        # Initialize Network and add nodes
        self.network = Network()
        self.network.add_node(self.node1)
        self.network.add_node(self.node2)

        # Initialize Consensus
        self.consensus = Consensus(self.blockchain)

    def test_genesis_block_creation(self):
        """
        Test the creation of the genesis block.
        """
        genesis_block = self.blockchain.get_genesis_block()
        self.assertEqual(
            genesis_block.index, 0,
            "[Genesis Block Creation Test] Expected genesis block index to be 0, but got {}".format(genesis_block.index)
        )
        self.assertEqual(
            genesis_block.previous_hash, "0" * 64,
            "[Genesis Block Creation Test] Expected genesis block previous hash to be all zeros, but got {}".format(genesis_block.previous_hash)
        )

    def test_transaction_creation(self):
        """
        Test creation and verification of transactions.
        """
        transaction = Transaction(sender="Alice", receiver="Bob", amount=10)
        transaction.sign_transaction("Alice_Private_Key")
        self.assertTrue(
            transaction.is_valid(),
            "[Transaction Creation Test] Expected transaction to be valid, but it was invalid."
        )

    def test_add_transaction_to_block(self):
        """
        Test adding a transaction to the blockchain and ensuring it gets added to a block.
        """
        transaction = Transaction(sender="Alice", receiver="Bob", amount=50)
        transaction.sign_transaction("Alice_Private_Key")

        self.blockchain.add_transaction(transaction)
        self.blockchain.mine_pending_transactions("Node_1")

        latest_block = self.blockchain.get_latest_block()
        self.assertTrue(
            transaction in latest_block.transactions,
            "[Add Transaction to Block Test] Expected transaction to be present in the latest block."
        )

    def test_block_mining(self):
        """
        Test that mining a block correctly updates the blockchain.
        """
        transaction = Transaction(sender="Alice", receiver="Bob", amount=25)
        transaction.sign_transaction("Alice_Private_Key")

        self.blockchain.add_transaction(transaction)
        mined_block = self.blockchain.mine_pending_transactions("Node_1")

        self.assertIsNotNone(
            mined_block,
            "[Block Mining Test] Expected mined block not to be None, but got None."
        )
        self.assertGreater(
            mined_block.index, 0,
            "[Block Mining Test] Expected mined block index to be greater than 0, but got {}".format(mined_block.index)
        )

    def test_consensus_mechanism(self):
        """
        Test consensus mechanism to ensure the longest valid chain is selected.
        """
        # Simulate Node_2 with a longer chain
        self.node2.blockchain.create_and_add_block(data="Node 2 Block 1")
        self.node2.blockchain.create_and_add_block(data="Node 2 Block 2")

        # Run consensus mechanism
        self.consensus.run()

        self.assertEqual(
            len(self.blockchain.chain), len(self.node2.blockchain.chain),
            "[Consensus Mechanism Test] Expected blockchain to adopt longest chain from Node_2."
        )

    def test_node_communication(self):
        """
        Test communication between nodes in the network.
        """
        self.node1.broadcast_transaction(Transaction(sender="Alice", receiver="Bob", amount=15))

        self.assertEqual(
            len(self.node2.blockchain.pending_transactions), 1,
            "[Node Communication Test] Expected Node_2 to have received 1 transaction, but got {}.".format(len(self.node2.blockchain.pending_transactions))
        )

    def test_validate_chain_integrity(self):
        """
        Test validation of the blockchain's integrity.
        """
        self.assertTrue(
            self.blockchain.is_chain_valid(),
            "[Validate Chain Integrity Test] Expected blockchain to be valid, but it was invalid."
        )

        # Tamper with blockchain data
        self.blockchain.chain[1].transactions[0].amount = 1000

        self.assertFalse(
            self.blockchain.is_chain_valid(),
            "[Validate Chain Integrity Test] Expected blockchain to be invalid after tampering, but it was valid."
        )

    def test_block_timestamps(self):
        """
        Test that each block in the blockchain has a unique timestamp.
        """
        transaction_1 = Transaction(sender="Alice", receiver="Bob", amount=10)
        transaction_1.sign_transaction("Alice_Private_Key")

        transaction_2 = Transaction(sender="Carol", receiver="Dave", amount=15)
        transaction_2.sign_transaction("Carol_Private_Key")

        self.blockchain.add_transaction(transaction_1)
        self.blockchain.mine_pending_transactions("Node_1")

        time.sleep(1)  # Ensure different timestamp

        self.blockchain.add_transaction(transaction_2)
        self.blockchain.mine_pending_transactions("Node_2")

        block_1 = self.blockchain.chain[1]
        block_2 = self.blockchain.chain[2]

        self.assertNotEqual(
            block_1.timestamp, block_2.timestamp,
            "[Block Timestamps Test] Expected block timestamps to be different, but got the same timestamp."
        )

    def test_fork_resolution(self):
        """
        Test that the blockchain can resolve forks correctly.
        """
        # Create two different chains on Node_1 and Node_2
        self.node1.blockchain.create_and_add_block(data="Node 1 Block A")
        self.node2.blockchain.create_and_add_block(data="Node 2 Block B")
        self.node2.blockchain.create_and_add_block(data="Node 2 Block C")

        # Run consensus to resolve fork
        self.consensus.run()

        self.assertEqual(
            len(self.blockchain.chain), len(self.node2.blockchain.chain),
            "[Fork Resolution Test] Expected blockchain to adopt Node_2's longer chain."
        )

    def test_reward_allocation(self):
        """
        Test that the miner receives rewards after successfully mining a block.
        """
        initial_balance = self.blockchain.get_balance("Node_1")

        self.blockchain.mine_pending_transactions("Node_1")
        new_balance = self.blockchain.get_balance("Node_1")

        self.assertGreater(
            new_balance, initial_balance,
            "[Reward Allocation Test] Expected Node_1's balance to increase after mining a block, but it did not."
        )

    def test_network_node_discovery(self):
        """
        Test that a node can discover other nodes in the network.
        """
        discovered_nodes = self.node1.discover_nodes()

        self.assertIn(
            self.node2.node_id, discovered_nodes,
            "[Network Node Discovery Test] Expected Node_1 to discover Node_2, but it did not."
        )

    def test_invalid_transaction_rejection(self):
        """
        Test that the blockchain correctly rejects invalid transactions.
        """
        invalid_transaction = Transaction(sender="Eve", receiver="Mallory", amount=5000)  # Invalid due to insufficient balance
        invalid_transaction.sign_transaction("Eve_Private_Key")

        self.blockchain.add_transaction(invalid_transaction)

        self.assertNotIn(
            invalid_transaction, self.blockchain.pending_transactions,
            "[Invalid Transaction Rejection Test] Expected invalid transaction to be rejected, but it was added to pending transactions."
        )


if __name__ == '__main__':
    unittest.main()

import unittest
from privacy_contracts import PrivacyContract
from quantum_tools import QuantumCrypto
from privacy_contracts import ZeroKnowledgeProof

class TestPrivacyContracts(unittest.TestCase):
    """
    Test Suite for Privacy Contracts in SypherLang
    This suite tests the correct execution and security features of privacy-related contracts.
    """

    def setUp(self):
        """
        Set up PrivacyContract and QuantumCrypto instances for testing.
        """
        self.privacy_contract = PrivacyContract()
        self.quantum_crypto = QuantumCrypto()
        self.zkp = ZeroKnowledgeProof()

    def test_data_encryption(self):
        """
        Test that the data is encrypted correctly.
        """
        data = "Sensitive Data"
        encrypted_data = self.privacy_contract.encrypt_data(data)
        self.assertNotEqual(
            data, encrypted_data,
            "[Data Encryption Test] Data should be encrypted. Expected encrypted value different from the original."
        )
        self.assertTrue(
            encrypted_data.startswith("encrypted_"),
            "[Data Encryption Test] Expected encrypted data to start with 'encrypted_', but got {}".format(encrypted_data)
        )

    def test_data_decryption(self):
        """
        Test that encrypted data is decrypted back to the original value.
        """
        data = "Sensitive Data"
        encrypted_data = self.privacy_contract.encrypt_data(data)
        decrypted_data = self.privacy_contract.decrypt_data(encrypted_data)
        self.assertEqual(
            data, decrypted_data,
            "[Data Decryption Test] Expected decrypted value to match the original data, but got {}".format(decrypted_data)
        )

    def test_zero_knowledge_proof_generation(self):
        """
        Test that a zero-knowledge proof is generated correctly.
        """
        data = "ProveThisData"
        proof = self.zkp.prove(data)
        self.assertIsNotNone(
            proof,
            "[ZKP Generation Test] Proof generation failed. Proof should not be None."
        )
        self.assertTrue(
            proof.startswith("zkp_proof_"),
            "[ZKP Generation Test] Expected proof to start with 'zkp_proof_', but got {}".format(proof)
        )

    def test_zero_knowledge_proof_verification(self):
        """
        Test that a zero-knowledge proof is verified successfully.
        """
        data = "ProveThisData"
        proof = self.zkp.prove(data)
        verification_result = self.zkp.verify(proof, data)
        self.assertTrue(
            verification_result,
            "[ZKP Verification Test] Expected proof verification to succeed, but it failed."
        )

    def test_data_sharing_privacy(self):
        """
        Test that data shared within the privacy contract is done securely.
        """
        data = "Confidential Info"
        encrypted_data = self.privacy_contract.encrypt_data(data)
        shared_data = self.privacy_contract.share_data(encrypted_data)
        self.assertTrue(
            shared_data.startswith("shared_encrypted_"),
            "[Data Sharing Privacy Test] Expected shared data to start with 'shared_encrypted_', but got {}".format(shared_data)
        )

    def test_quantum_resistant_encryption(self):
        """
        Test the quantum-resistant encryption provided by QuantumCrypto.
        """
        data = "QuantumSafeData"
        secure_key = self.quantum_crypto.generate_quantum_resistant_key()
        encrypted_data = self.quantum_crypto.encrypt(data, secure_key)
        self.assertNotEqual(
            data, encrypted_data,
            "[Quantum Resistant Encryption Test] Expected encrypted data to differ from original."
        )
        self.assertTrue(
            encrypted_data.startswith("lattice_encrypted_"),
            "[Quantum Resistant Encryption Test] Expected encrypted data to start with 'lattice_encrypted_', but got {}".format(encrypted_data)
        )

    def test_quantum_resistant_decryption(self):
        """
        Test the decryption of quantum-resistant encrypted data.
        """
        data = "QuantumSafeData"
        secure_key = self.quantum_crypto.generate_quantum_resistant_key()
        encrypted_data = self.quantum_crypto.encrypt(data, secure_key)
        decrypted_data = self.quantum_crypto.decrypt(encrypted_data, secure_key)
        self.assertEqual(
            data, decrypted_data,
            "[Quantum Resistant Decryption Test] Expected decrypted data to match original data, but got {}".format(decrypted_data)
        )

    def test_privacy_contract_execution(self):
        """
        Test the execution of a privacy contract involving encryption and zero-knowledge proof.
        """
        data = "ExecutePrivacy"
        contract_result = self.privacy_contract.execute_privacy_contract(data)
        self.assertTrue(
            "encrypted_" in contract_result and "zkp_proof_" in contract_result,
            "[Privacy Contract Execution Test] Expected result to contain both encrypted data and proof, but got {}".format(contract_result)
        )

    def test_access_control_privacy_contract(self):
        """
        Test that access control mechanisms are applied within the privacy contract.
        """
        user_role = "user"
        result = self.privacy_contract.access_control("Sensitive Data", user_role)
        self.assertEqual(
            result, "Access Denied",
            "[Access Control Privacy Test] Expected 'Access Denied' for 'user' role, but got {}".format(result)
        )
        
        admin_role = "admin"
        result = self.privacy_contract.access_control("Sensitive Data", admin_role)
        self.assertNotEqual(
            result, "Access Denied",
            "[Access Control Privacy Test] Expected 'Access Granted' for 'admin' role, but got 'Access Denied'"
        )

    def test_invalid_proof_verification(self):
        """
        Test that an invalid proof does not pass verification.
        """
        data = "InvalidProof"
        proof = "invalid_zkp_proof"
        verification_result = self.zkp.verify(proof, data)
        self.assertFalse(
            verification_result,
            "[Invalid Proof Verification Test] Expected proof verification to fail for an invalid proof, but it passed."
        )

    def test_privacy_integration_with_blockchain(self):
        """
        Test the integration of privacy contracts with SypherCore blockchain.
        """
        data = "BlockchainPrivacy"
        encrypted_data = self.privacy_contract.encrypt_data(data)
        proof = self.zkp.prove(encrypted_data)
        transaction = {
            "data": encrypted_data,
            "proof": proof,
            "sender": "0xSenderAddress",
            "receiver": "0xReceiverAddress"
        }
        # Simulate adding a transaction to the blockchain
        blockchain_result = self.privacy_contract.add_transaction(transaction)
        self.assertEqual(
            blockchain_result, "Transaction Added",
            "[Privacy Integration Test] Expected transaction to be added to blockchain, but it failed."
        )

    def test_smart_contract_data_retrieval(self):
        """
        Test that encrypted data within a privacy contract can be retrieved correctly.
        """
        data = "RetrieveThisData"
        encrypted_data = self.privacy_contract.encrypt_data(data)
        self.privacy_contract.store_data("contract1", encrypted_data)
        retrieved_data = self.privacy_contract.retrieve_data("contract1")
        self.assertEqual(
            retrieved_data, encrypted_data,
            "[Smart Contract Data Retrieval Test] Expected to retrieve the encrypted data, but got {}".format(retrieved_data)
        )


if __name__ == '__main__':
    unittest.main()

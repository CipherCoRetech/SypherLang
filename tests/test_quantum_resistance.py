import unittest
from quantum_tools import QuantumCrypto


class TestQuantumResistance(unittest.TestCase):
    """
    Test Suite for Quantum-Resistant Cryptographic Features in SypherLang
    This suite tests the encryption and decryption functionality of QuantumCrypto
    to ensure quantum resistance and security.
    """

    def setUp(self):
        """
        Set up QuantumCrypto instance for testing.
        """
        self.quantum_crypto = QuantumCrypto()

    def test_generate_quantum_resistant_key(self):
        """
        Test generation of a quantum-resistant key.
        """
        secure_key = self.quantum_crypto.generate_quantum_resistant_key()
        self.assertIsNotNone(
            secure_key,
            "[Quantum Key Generation Test] Expected key generation to return a non-null key, but got None."
        )
        self.assertTrue(
            secure_key.startswith("lattice_key_"),
            "[Quantum Key Generation Test] Expected key to start with 'lattice_key_', but got {}".format(secure_key)
        )

    def test_encryption_with_generated_key(self):
        """
        Test encryption of data with a quantum-resistant key.
        """
        data = "QuantumSensitiveData"
        secure_key = self.quantum_crypto.generate_quantum_resistant_key()
        encrypted_data = self.quantum_crypto.encrypt(data, secure_key)
        self.assertNotEqual(
            data, encrypted_data,
            "[Encryption with Generated Key Test] Expected encrypted data to differ from original data."
        )
        self.assertTrue(
            encrypted_data.startswith("lattice_encrypted_"),
            "[Encryption with Generated Key Test] Expected encrypted data to start with 'lattice_encrypted_', but got {}".format(encrypted_data)
        )

    def test_decryption_with_generated_key(self):
        """
        Test decryption of encrypted data with the same quantum-resistant key.
        """
        data = "QuantumSensitiveData"
        secure_key = self.quantum_crypto.generate_quantum_resistant_key()
        encrypted_data = self.quantum_crypto.encrypt(data, secure_key)
        decrypted_data = self.quantum_crypto.decrypt(encrypted_data, secure_key)
        self.assertEqual(
            data, decrypted_data,
            "[Decryption with Generated Key Test] Expected decrypted data to match original data, but got {}".format(decrypted_data)
        )

    def test_incorrect_key_decryption(self):
        """
        Test that decryption fails when an incorrect key is used.
        """
        data = "QuantumSensitiveData"
        secure_key = self.quantum_crypto.generate_quantum_resistant_key()
        encrypted_data = self.quantum_crypto.encrypt(data, secure_key)

        # Generate another key to simulate incorrect key usage
        incorrect_key = self.quantum_crypto.generate_quantum_resistant_key()

        decrypted_data = self.quantum_crypto.decrypt(encrypted_data, incorrect_key)
        self.assertNotEqual(
            data, decrypted_data,
            "[Incorrect Key Decryption Test] Expected decryption with incorrect key to fail, but data matches the original."
        )
        self.assertEqual(
            decrypted_data, "Decryption Failed",
            "[Incorrect Key Decryption Test] Expected decryption with incorrect key to fail, but got {}".format(decrypted_data)
        )

    def test_large_data_encryption(self):
        """
        Test encryption and decryption of a large dataset to ensure scalability.
        """
        large_data = "QuantumData" * 1000  # Simulate a large dataset
        secure_key = self.quantum_crypto.generate_quantum_resistant_key()
        encrypted_data = self.quantum_crypto.encrypt(large_data, secure_key)
        decrypted_data = self.quantum_crypto.decrypt(encrypted_data, secure_key)

        self.assertEqual(
            large_data, decrypted_data,
            "[Large Data Encryption Test] Expected decrypted large data to match original data, but got mismatch."
        )

    def test_quantum_resistance_against_attack(self):
        """
        Simulate a quantum attack and ensure that the encryption is resistant.
        """
        data = "QuantumSafeData"
        secure_key = self.quantum_crypto.generate_quantum_resistant_key()
        encrypted_data = self.quantum_crypto.encrypt(data, secure_key)

        # Simulate quantum attack
        quantum_attack_result = self.quantum_crypto.simulate_quantum_attack(encrypted_data)
        self.assertFalse(
            quantum_attack_result,
            "[Quantum Resistance Test] Expected encryption to be resistant against quantum attack, but it failed."
        )

    def test_key_derivation_security(self):
        """
        Test that key derivation is secure and that derived keys do not match.
        """
        base_key = "BaseSecureKey"
        derived_key_1 = self.quantum_crypto.derive_key(base_key, "context1")
        derived_key_2 = self.quantum_crypto.derive_key(base_key, "context2")

        self.assertNotEqual(
            derived_key_1, derived_key_2,
            "[Key Derivation Security Test] Expected derived keys with different contexts to be unique, but got identical keys."
        )
        self.assertTrue(
            derived_key_1.startswith("derived_lattice_key_") and derived_key_2.startswith("derived_lattice_key_"),
            "[Key Derivation Security Test] Expected derived keys to start with 'derived_lattice_key_', but got {} and {}".format(derived_key_1, derived_key_2)
        )

    def test_invalid_key_handling(self):
        """
        Test the behavior when an invalid or malformed key is used for decryption.
        """
        data = "SecureData"
        secure_key = self.quantum_crypto.generate_quantum_resistant_key()
        encrypted_data = self.quantum_crypto.encrypt(data, secure_key)

        invalid_key = "invalid_key"
        decrypted_data = self.quantum_crypto.decrypt(encrypted_data, invalid_key)

        self.assertEqual(
            decrypted_data, "Decryption Failed",
            "[Invalid Key Handling Test] Expected decryption with an invalid key to fail, but got {}".format(decrypted_data)
        )

    def test_zero_knowledge_proof_integration(self):
        """
        Test the integration of zero-knowledge proofs with quantum-resistant encryption.
        """
        data = "ZKPTestData"
        secure_key = self.quantum_crypto.generate_quantum_resistant_key()
        encrypted_data = self.quantum_crypto.encrypt(data, secure_key)
        
        proof = self.quantum_crypto.generate_proof(encrypted_data)
        verification_result = self.quantum_crypto.verify_proof(proof, encrypted_data)

        self.assertTrue(
            verification_result,
            "[Zero-Knowledge Proof Integration Test] Expected zero-knowledge proof to verify successfully, but it failed."
        )

    def test_performance_of_quantum_encryption(self):
        """
        Measure the time taken for encryption and decryption of a dataset to ensure performance is acceptable.
        """
        import time
        data = "PerformanceTestData" * 100

        secure_key = self.quantum_crypto.generate_quantum_resistant_key()

        # Measure encryption time
        start_time = time.time()
        encrypted_data = self.quantum_crypto.encrypt(data, secure_key)
        encryption_time = time.time() - start_time

        # Measure decryption time
        start_time = time.time()
        decrypted_data = self.quantum_crypto.decrypt(encrypted_data, secure_key)
        decryption_time = time.time() - start_time

        self.assertLess(
            encryption_time, 1.0,
            "[Performance Test] Expected encryption to take less than 1 second, but it took {:.2f} seconds.".format(encryption_time)
        )
        self.assertLess(
            decryption_time, 1.0,
            "[Performance Test] Expected decryption to take less than 1 second, but it took {:.2f} seconds.".format(decryption_time)
        )


if __name__ == '__main__':
    unittest.main()

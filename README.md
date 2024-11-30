# SypherLang

**SypherLang** is a domain-specific programming language tailored for the creation and management of decentralized, quantum-resistant applications and privacy-focused smart contracts. It is developed with advanced cryptographic concepts such as Zero-Knowledge Proofs (ZKP) and lattice-based cryptography for enhanced security and privacy in blockchain technology. This repository contains the SypherLang source code and detailed documentation to guide developers through using the language effectively.

## Overview

SypherLang is built with the following core features:

1. **Privacy-Focused Smart Contracts**: Enabling developers to create contracts that protect user data and maintain privacy through advanced cryptographic protocols.
2. **Quantum-Resistant Security**: The integration of lattice-based cryptographic primitives ensures SypherLang remains secure in a post-quantum computing world.
3. **Concurrency & Parallel Processing**: Utilizing parallel processing for high-performance decentralized application execution.
4. **Zero-Knowledge Proofs**: The language includes built-in support for ZKPs to allow verification of information without revealing sensitive data.
5. **Rich Developer Tools**: The SypherLang IDE and compiler make the development process intuitive and streamlined.

## Directory Structure

Below is the folder structure of SypherLang and their descriptions:

- **compiler**: Contains the lexer, parser, and AST generation tools for translating SypherLang code into executable instructions.
- **concurrency**: Holds modules related to concurrent execution, including `parallel_exec.py` for task parallelism.
- **examples**: Code examples that demonstrate different use-cases for SypherLang.
- **ide**: The Integrated Development Environment (IDE) that provides a graphical interface for writing and executing SypherLang programs.
- **interpreter**: The interpreter executes compiled SypherLang code, allowing dynamic evaluation of code and expressions.
- **privacy_contracts**: Cryptographic contracts, including tools for Zero-Knowledge Proofs (`prove.py`, `verify.py`, `zkp.py`).
- **quantum_resistance**: Cryptographic modules that implement quantum-resistant cryptographic functions such as lattice-based encryption (`lattice_crypto.py`).

## Installation

### Prerequisites

To install and use SypherLang, you need:

- Python 3.8+
- Docker (for executing blockchain nodes)
- Git

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/SypherCoRe/SypherLang.git
   cd SypherLang
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the SypherLang IDE (optional, but recommended for a richer development experience):
   ```bash
   python setup.py install
   ```

4. To run your first SypherLang program, navigate to the `examples` directory:
   ```bash
   cd examples
   python run_example.py
   ```

## Quick Start

Here’s a simple example of SypherLang syntax for creating a privacy-focused smart contract:

```sypher
contract ConfidentialToken {
    public int totalSupply;
    private mapping (address => uint) balances;

    function mint(address recipient, uint amount) private {
        balances[recipient] += amount;
        totalSupply += amount;
    }

    function balanceOf(address owner) public view returns (uint) {
        return balances[owner];
    }
}
```

The above contract defines a token with privacy features, such as hiding individual balances, and only allowing trusted operations by designated functions.

## Using the IDE

The SypherLang IDE is designed to make developing decentralized, privacy-focused applications simple and efficient. Key features include:

- **Syntax Highlighting**: Recognizes SypherLang constructs for easier readability.
- **Integrated Debugger**: Allows step-by-step execution of code to identify issues.
- **Blockchain Integration**: Deploy your contracts directly to the blockchain from the IDE.

To launch the IDE:
```bash
python ide/sypherlang_ide.py
```

## Contributing

We welcome contributions from the open-source community! To get started:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a Pull Request and describe the changes you’ve made.

## Quantum Resistance

SypherLang includes **lattice-based cryptographic algorithms** to resist quantum computing threats. The `quantum_resistance` folder holds implementations such as `lattice_crypto.py`, which ensure the security of contracts and blockchain applications even in a post-quantum scenario.

### Example - Lattice-Based Key Exchange

The following SypherLang script demonstrates a lattice-based key exchange:

```sypher
lattice_keypair alice;
lattice_keypair bob;

exchange_key(alice, bob);
```

This script creates quantum-resistant keys for Alice and Bob, allowing them to communicate securely.

## Zero-Knowledge Proofs (ZKPs)

SypherLang has built-in support for **Zero-Knowledge Proofs** to enhance privacy. With `prove.py` and `verify.py`, developers can implement ZKP to prove possession of knowledge without revealing the underlying information.

Example:
```sypher
proof zkProof = prove(secretValue);
verify(zkProof);
```

The `zkp.py` script provides the underlying cryptographic primitives for these operations.

## License

SypherLang is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/SypherCoRe/SypherLang/issues).

You can also contact the core team via email: `support@syphercore.com`

## Roadmap

- **Mainnet Launch**: Deploy SypherLang contracts on a public mainnet.
- **IDE Enhancements**: Adding more developer tools, such as linting and auto-formatting.
- **Smart Contract Templates**: Provide out-of-the-box templates for popular use-cases.

# CypherLang API Reference

## Overview
CypherLang provides a comprehensive API for compiling, deploying, and executing contracts.

## Compiler API
### `compile(source_code: str) -> bytecode`
Compiles CypherLang source code into bytecode.
- **Parameters**:
  - `source_code`: A string containing the source code.
- **Returns**:
  - The compiled bytecode.

## Runtime API
### `execute(bytecode: str, inputs: dict) -> dict`
Executes CypherLang bytecode in the virtual machine.
- **Parameters**:
  - `bytecode`: A string of compiled bytecode.
  - `inputs`: A dictionary of input values.
- **Returns**:
  - A dictionary with execution results.

## Standard Library
### Math Module
- `add(a: int, b: int) -> int`
- `multiply(a: int, b: int) -> int`

### Crypto Module
- `hash(data: str) -> str`
- `verify_signature(data: str, signature: str, public_key: str) -> bool`


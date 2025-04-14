Smart Contract Scanner - AI-Agent

This Python script provides a dual-mode smart contract scanning tool that interfaces with two Solidity Scan APIs to analyse smart contracts for security vulnerabilities and threats. It supports two operational modes:

Direct API Test: Directly interacts with the Solidity Scan APIs to perform scans, allowing administrators to input parameters and view raw API responses.

Agent: Utilising G.A.M.E SDK an AI-Agent-based system (with a worker configuration) to guide users through the scanning process by collecting parameters interactively.

The script supports two types of scans:

Vulnerability Scan (v1 API): Identifies vulnerabilities, security risks, and optimisation opportunities in smart contracts.

Threat Scan (v2 API): Performs specialised threat analysis, which may return an initialisation response for asynchronous processing.

Features

Supports multiple blockchain platforms (e.g., Etherscan, BSCScan, PolygonScan, Basescan, etc.).

Comprehensive chain support across various platforms (mainnet, testnet, and more).

Interactive parameter collection for user-friendly scanning.

Detailed scan results with severity distributions, scores, and reference URLs.

Error handling with retry logic for API requests.

Environment variable support for secure API key management.

Prerequisites

Python 3.8 or higher

Required Python packages:

requests

game_sdk (custom SDK for agent-based functionality)

API Keys:

Solidity Scan API key (SOLIDITYSCAN_API_KEY)

Game SDK API key (GAME_API_KEY) for Agent mode

Installation

Clone the repository (or download the script):

git clone <repository-url>
cd <repository-directory>

Install dependencies:

pip install requests

Note: The game_sdk package is assumed to be a custom or proprietary SDK. Ensure it is installed or available in your environment.

Set up environment variables:

Set your API keys as environment variables:

export SOLIDITYSCAN_API_KEY="your_solidityscan_api_key"
export GAME_API_KEY="your_game_api_key"

On Windows, use:

cmd

set SOLIDITYSCAN_API_KEY=your_solidityscan_api_key
set GAME_API_KEY=your_game_api_key

Usage

Run the script using Python:

python smart_contract_scanner.py

Main Menu

Upon running, you will see a menu with three options:

Direct API Test: Test the Solidity Scan API directly by manually entering scan parameters.

Agent: Interact with the agent, which guides you through the scanning process step-by-step.

Exit: Quit the program.

Direct API Test

Select scan type (Vulnerability Scan or Threat Scan).

Choose a platform ID from the listed options (e.g., 17 for Basescan).

Select a chain ID (e.g., 1 for mainnet).

Enter the contract address (must start with 0x).

View scan results, with an option to see the full JSON response.

Press Enter to return to the main menu.

Agent

Express interest in scanning a contract (e.g., type "scan contract").

Select scan type (1 for Vulnerability Scan, 2 for Threat Scan).

Provide platform ID, chain ID, and contract address when prompted.

View scan results, with an option to see the full JSON response.

Press Enter to return to the main menu.

Type exit at any time to quit the agent test.

Supported Platforms

The script supports a wide range of platforms, including:

Etherscan (1)

BSCScan (2)

PolygonScan (3)

Basescan (17)

Tronscan (19)

And many others (see full list in the script's platforms state).

Each platform supports specific chains (e.g., mainnet, testnet, or custom chains like Sepolia).

Scan Output

Vulnerability Scan:

Risk level, score, and rating

Counts of critical, high, medium, and low vulnerabilities

Security risks, optimisation opportunities, and informational issues

Contract name, URL, scan type, and detailed scan URL

Threat Scan:

Initialisation response (scan ID, status) or complete results

Threat score, scan status, and severity counts (Beneficial, Low Risk, etc.)

Pass/fail/skipped issue counts and detailed scan URL

Example

Direct API Test Example

Smart Contract Scanner - Dual Test Suite
--------------------------------------
Select a mode:
1. Direct API Test
2. Agent
3. Exit

Enter your choice (1-3): 1

Smart Contract Scanner - Direct API Test
--------------------------------------
Step 0: Select scan type
1. Vulnerability Scan (v1 API)
2. Threat Scan (v2 API)

Enter scan type (1 or 2): 1
Selected Scan Type: Vulnerability Scan

Step 1: Select a platform
Available Platforms:
- etherscan.io (ID: 1)
- bscscan.com (ID: 2)
- basescan.org (ID: 17)
...

Enter Platform ID: 17
Selected Platform: basescan.org (ID: 17)

Step 2: Select a chain
Available Chains for this platform:
- mainnet (ID: 1)
- testnet (ID: 2)

Enter Chain ID: 1
Selected Chain: mainnet (ID: 1)

Step 3: Enter contract address
Enter Contract Address (must start with 0x): 0x1234...

Agent Example

Enter your choice (1-3): 2

Smart Contract Scanner - Agent
--------------------------------------
Agent is ready. You can now interact with it.
First, express your interest in conducting a smart contract scan.
Type 'exit' to quit the test.

You: I want to scan a smart contract

Step 0: Select scan type
1. Vulnerability Scan (v1 API)
2. Threat Scan (v2 API)

Enter scan type (1 or 2): 1
Selected Scan Type: Vulnerability Scan

Step 1: Select a platform
Available Platforms:
- etherscan.io (ID: 1)
- bscscan.com (ID: 2)
- basescan.org (ID: 17)
...

Enter Platform ID: 17
...

Notes
Threat Scan Limitations: The v2 API for threat scans may return an initialisation response, indicating that results will be delivered asynchronously to configured endpoints. Check the Solidity Scan documentation for details on retrieving these results.

API Key Security: Store API keys securely in environment variables, not in the script or version control.

Error Handling: The script includes retry logic for API timeouts and validates inputs (e.g., contract address format).

Extensibility: The script's state management supports adding new platforms and chains easily.

Contributing

Feel free to submit issues or pull requests to improve the script. Suggestions for new features, bug fixes, or additional platform support are welcome.

License

This project is licensed under the MIT License. 

Acknowledgments

Built with the Solidity Scan Vulnerability and Threat Scan APIs for smart contract scanning.

Uses the game_sdk for agent-based functionality.

Comprehensive platform and chain data sourced from Solidity Scan's parameters.

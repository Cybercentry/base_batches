Smart Contract Scanner

This Python script is a standalone tool for scanning smart contracts using the SolidityScan APIs to identify security vulnerabilities and threats. It interacts directly with the SolidityScan APIs, allowing users to input parameters and view detailed scan results. The script supports three types of scans:

Vulnerability Scan (v1 API): Identifies vulnerabilities, security risks, and optimization opportunities in smart contracts.

Threat Scan (v2 API): Performs specialized threat analysis, which may return an initialization response for asynchronous processing or complete results.

Combined Scan: Runs both vulnerability and threat scans, combining results for a comprehensive analysis.

Features Supports multiple blockchain platforms (e.g., Etherscan, BSCScan, PolygonScan, Basescan, Tronscan, etc.).

Comprehensive chain support across various platforms (mainnet, testnet, and custom chains like Sepolia).

Interactive command-line interface for selecting scan type, platform, chain, and contract address.

Detailed scan results with severity distributions, scores, and reference URLs.

Robust error handling with retry logic for API requests (up to 3 retries with exponential backoff).

Environment variable support for secure API key management.

Option to view full JSON responses for in-depth analysis.

Prerequisites Python 3.8 or higher

Required Python packages: requests

API Key: SolidityScan API key (SOLIDITYSCAN_API_KEY)

Installation Clone the repository (or download the script):

git clone cd

Install dependencies:

pip install requests

Set up environment variables: Set your SolidityScan API key as an environment variable: On Linux/macOS:

export SOLIDITYSCAN_API_KEY="your_solidityscan_api_key"

On Windows (Command Prompt):

set SOLIDITYSCAN_API_KEY=your_solidityscan_api_key

Usage Run the script using Python:

python smart_contract_scanner.py

Scanning Process Select Scan Type: Choose from: Vulnerability Scan (v1 API)

Threat Scan (v2 API)

Combined Scan (Both)

Exit

Select Platform: View a list of supported platforms (e.g., etherscan.io (ID: 1), basescan.org (ID: 17)).

Enter the platform ID.

Select Chain: View available chains for the selected platform (e.g., mainnet (ID: 1), testnet (ID: 2)).

Enter the chain ID.

Enter Contract Address: Provide a valid contract address (must start with 0x).

View Results: See a summary of scan results, including severity counts, scores, and reference URLs.

Optionally view the full JSON response.

Choose to scan another contract or exit.

Supported Platforms The script supports 24 platforms, including: Etherscan (ID: 1)

BSCScan (ID: 2)

PolygonScan (ID: 3)

Basescan (ID: 17)

Tronscan (ID: 19)

Lineascan (ID: 21)

And many others (see full list in the script).

Each platform supports specific chains, such as mainnet, testnet, or custom chains like Sepolia or Shasta. Scan Output Vulnerability Scan Risk level, score, and rating (e.g., "High", "8.5/10", "Good")

Counts of critical, high, medium, and low vulnerabilities

Security risks, optimization opportunities, and informational issues

Contract name, URL, scan type, lines analyzed, and detailed scan URL

Threat Scan Initialization Response (if asynchronous): Scan ID, status, request UUID, and total detectors

Complete Results: Threat score, scan status

Severity counts (Beneficial, No Impact, Low Risk, Moderate Risk, High Risk, Unavailable)

Pass/fail/skipped issue counts

Detailed scan URL

Combined Scan Combines vulnerability and threat scan results

Includes all metrics from both scans (e.g., vulnerability counts, threat score, severity distributions)

Indicates if both scans were successful

Provides separate URLs for vulnerability and threat scan results

Example

Standalone Smart Contract Scanner
Using SolidityScan API Key: abcd...wxyz

Step 0: Select scan type

Vulnerability Scan (v1 API)
Threat Scan (v2 API)
Combined Scan (Both)
Exit
Enter scan type (1-4): 3 Selected Scan Type: Combined Scan

Step 1: Select a platform Available Platforms:

etherscan.io (ID: 1)
bscscan.com (ID: 2)
basescan.org (ID: 17) ...
Enter Platform ID: 17 Selected Platform: basescan.org (ID: 17)

Step 2: Select a chain Available Chains for this platform:

mainnet (ID: 1)
testnet (ID: 2)
Enter Chain ID: 1 Selected Chain: mainnet (ID: 1)

Step 3: Enter contract address Enter Contract Address (must start with 0x): 0x1234...

Performing combined scan on contract 0x1234... on basescan.org (Platform ID: 17, Chain ID: 1)...

Scan Status: DONE Message: Successfully completed both vulnerability and threat scans for contract 0x1234...

Scan Results:

Contract Name: ExampleContract
Both Scans Successful: True
Vulnerability Scan Results:
Score: 8.5 (Good)
Total Vulnerabilities: 5
Security Risks: 2
Optimization Opportunities: 1
Informational Issues: 2
Threat Scan Results:
Threat Score: 75
Issues by Severity:
Beneficial: 1
No Impact: 2
Low Risk: 1
Moderate Risk: 0
High Risk: 0
Unavailable: 0
Issue Status:
Pass: 3
Fail: 1
Skipped: 0
Vulnerability scan results available at: https://solidityscan.com/report/... Threat scan results available at: https://solidityscan.com/report/...

Do you want to see the full JSON response? (yes/no): no Do you want to scan another contract? (yes/no): no Exiting...

Notes Threat Scan Limitations: The v2 API for threat scans may return an initialization response, indicating asynchronous processing. Results are pushed to configured endpoints or must be retrieved separately. Check the SolidityScan documentation for details.

API Key Security: Store the SOLIDITYSCAN_API_KEY securely in environment variables, not in the script or version control.

Error Handling: The script validates inputs (e.g., contract address format) and includes retry logic for API timeouts.

Extensibility: The script's platform and chain data can be easily updated to support new blockchains.

Next Steps The next phase of development involves enhancing the scanner by integrating it with the Base AgentKit. This will introduce an AI-agent-based interface to streamline user interactions, guide users through the scanning process with natural language prompts, and potentially automate parameter selection and result interpretation. The Base AgentKit will replace the current command-line interface with a more intuitive and user-friendly experience, making the tool accessible to a broader audience, including those with limited technical expertise.

Contributing Submit issues or pull requests to improve the script. Suggestions for new features, bug fixes, or additional platform support are welcome.

Acknowledgments Built with the SolidityScan Vulnerability Nancy (v1 and v2 APIs) for smart contract scanning.

Comprehensive platform and chain data sourced from SolidityScan's parameters.

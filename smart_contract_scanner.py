"""
Cybercentry - Smart Contract Scanner - AI Agent
"""

import os
import requests
import json
import time
import traceback
from enum import Enum
from typing import Tuple, Dict, Any, List, Optional

# Get API key from environment variables
solidityscan_api_key = os.environ.get("SOLIDITYSCAN_API_KEY")

# Define a simple enum for function result status
class FunctionResultStatus(Enum):
    DONE = "DONE"
    FAILED = "FAILED"

#######################
# Platform and Chain Data
#######################

def get_platforms_and_chains():
    """
    Returns the list of platforms and chains supported by SolidityScan.
    """
    platforms = [
        {"id": "1", "name": "etherscan.io"},
        {"id": "2", "name": "bscscan.com"},
        {"id": "3", "name": "polygonscan.com"},
        {"id": "4", "name": "snowtrace.io"},
        {"id": "5", "name": "ftmscan.com"},
        {"id": "6", "name": "cronoscan.com"},
        {"id": "7", "name": "celoscan.io"},
        {"id": "8", "name": "aurorascan.dev"},
        {"id": "9", "name": "arbiscan.io"},
        {"id": "10", "name": "buildbear"},
        {"id": "11", "name": "optimism"},
        {"id": "12", "name": "xdc"},
        {"id": "13", "name": "reefscan.com"},
        {"id": "14", "name": "nordekscan.com"},
        {"id": "15", "name": "explorer.fuse.io"},
        {"id": "16", "name": "blockscout.com"},
        {"id": "17", "name": "basescan.org"},
        {"id": "18", "name": "routescan"},
        {"id": "19", "name": "tronscan.org"},
        {"id": "21", "name": "lineascan.build"},
        {"id": "22", "name": "5irescan.io"},
        {"id": "23", "name": "subscan.io"},
        {"id": "24", "name": "opbnb"}
    ]
    
    chains = [
        # Ethereum (1)
        {"platform_id": "1", "id": "1", "name": "mainnet"},
        {"platform_id": "1", "id": "4", "name": "kovan"},
        {"platform_id": "1", "id": "5", "name": "rinkeby"},
        {"platform_id": "1", "id": "6", "name": "ropsten"},
        
        # BSC (2)
        {"platform_id": "2", "id": "1", "name": "mainnet"},
        {"platform_id": "2", "id": "2", "name": "testnet"},
        
        # Polygon (3)
        {"platform_id": "3", "id": "1", "name": "mainnet"},
        {"platform_id": "3", "id": "2", "name": "testnet"},
        
        # Avalanche (4)
        {"platform_id": "4", "id": "1", "name": "mainnet"},
        {"platform_id": "4", "id": "2", "name": "testnet"},
        
        # Fantom (5)
        {"platform_id": "5", "id": "1", "name": "mainnet"},
        {"platform_id": "5", "id": "2", "name": "testnet"},
        
        # Cronos (6)
        {"platform_id": "6", "id": "1", "name": "mainnet"},
        {"platform_id": "6", "id": "2", "name": "testnet"},
        
        # Celo (7)
        {"platform_id": "7", "id": "1", "name": "mainnet"},
        {"platform_id": "7", "id": "2", "name": "testnet"},
        
        # Aurora (8)
        {"platform_id": "8", "id": "1", "name": "mainnet"},
        {"platform_id": "8", "id": "2", "name": "testnet"},
        
        # Arbitrum (9)
        {"platform_id": "9", "id": "1", "name": "mainnet"},
        {"platform_id": "9", "id": "2", "name": "testnet"},
        
        # Reef (13)
        {"platform_id": "13", "id": "1", "name": "mainnet"},
        {"platform_id": "13", "id": "2", "name": "testnet"},
        
        # Nordek (14)
        {"platform_id": "14", "id": "1", "name": "mainnet"},
        
        # Fuse (15)
        {"platform_id": "15", "id": "1", "name": "mainnet"},
        {"platform_id": "15", "id": "2", "name": "testnet"},
        
        # Blockscout (16) - Many chains
        {"platform_id": "16", "id": "1", "name": "ETC Mainnet"},
        {"platform_id": "16", "id": "2", "name": "ETC Mordor"},
        {"platform_id": "16", "id": "3", "name": "ETH Mainnet"},
        {"platform_id": "16", "id": "5", "name": "ETH Sepolia"},
        {"platform_id": "16", "id": "6", "name": "ETH Holesky"},
        {"platform_id": "16", "id": "7", "name": "Base Mainnet"},
        {"platform_id": "16", "id": "8", "name": "Base Goerli"},
        {"platform_id": "16", "id": "9", "name": "Base Sepolia"},
        # ... and many more chains for platform 16
        
        # Basescan (17)
        {"platform_id": "17", "id": "1", "name": "mainnet"},
        {"platform_id": "17", "id": "2", "name": "testnet"},
        
        # Tron (19)
        {"platform_id": "19", "id": "1", "name": "Mainnet"},
        {"platform_id": "19", "id": "8", "name": "shasta"},
        {"platform_id": "19", "id": "9", "name": "nile"},
        
        # Linea (21)
        {"platform_id": "21", "id": "1", "name": "Mainnet"},
        {"platform_id": "21", "id": "4", "name": "Sepolia"},
        
        # 5ire (22)
        {"platform_id": "22", "id": "1", "name": "Mainnet"},
        
        # Subscan (23)
        {"platform_id": "23", "id": "1", "name": "astar-mainnet"},
        {"platform_id": "23", "id": "2", "name": "astar-shiden-mainnet"},
        {"platform_id": "23", "id": "3", "name": "astar-shibuya-testnet"},
        {"platform_id": "23", "id": "4", "name": "moonbeam-mainnet"},
        {"platform_id": "23", "id": "5", "name": "moonriver-mainnet"},
        {"platform_id": "23", "id": "6", "name": "moonbase-testnet"},
        {"platform_id": "23", "id": "7", "name": "peaq-mainnet"},
        {"platform_id": "23", "id": "8", "name": "krest-mainnet"},
        {"platform_id": "23", "id": "9", "name": "agung-testnet"},
        {"platform_id": "23", "id": "10", "name": "darwinia-mainnet"},
        {"platform_id": "23", "id": "11", "name": "polkadot-mainnet"},
        
        # opBNB (24)
        {"platform_id": "24", "id": "1", "name": "mainnet"},
        {"platform_id": "24", "id": "2", "name": "testnet"}
    ]
    
    return platforms, chains

def get_platform_chain_info(platform_id=None, chain_id=None):
    """Helper function to get platform and chain information."""
    platforms, chains = get_platforms_and_chains()
    result = {}
    
    # Look up platform info
    if platform_id:
        for platform in platforms:
            if platform["id"] == platform_id:
                result["platform"] = platform
                break
    
    # Look up chain info
    if platform_id and chain_id:
        for chain in chains:
            if chain["platform_id"] == platform_id and chain["id"] == chain_id:
                result["chain"] = chain
                break
    
    return result

#######################
# Scanning Functions
#######################

def vulnerability_scan(platform_id: str, chain_id: str, contract_address: str) -> Tuple[FunctionResultStatus, str, dict]:
    """
    Function to scan a smart contract for vulnerabilities.
    Uses the v1 API endpoint for vulnerability scanning.
    """
    if not all([platform_id, chain_id, contract_address]):
        return FunctionResultStatus.FAILED, "Missing required parameters", {}
    
    # Validate contract address format
    if not contract_address.startswith("0x"):
        return FunctionResultStatus.FAILED, "Invalid contract address format. Address must start with '0x'", {}
    
    try:
        # Get platform and chain info
        info = get_platform_chain_info(platform_id, chain_id)
        
        platform_name = info.get("platform", {}).get("name", "Unknown Platform")
        chain_name = info.get("chain", {}).get("name", "Unknown Chain")
        
        # Construct the API URL
        api_url = f"https://api.solidityscan.com/api/v1/quickscan/{platform_id}/{chain_id}/{contract_address}"
        
        print(f"Making API request to: {api_url}")
        
        # Set up headers with API key
        headers = {
            "Authorization": f"Token {solidityscan_api_key}",
            "Content-Type": "application/json"
        }
        
        # Make the API request with retry logic
        max_retries = 3
        retry_count = 0
        retry_delay = 5  # seconds
        
        while retry_count < max_retries:
            try:
                response = requests.get(api_url, headers=headers, timeout=60)
                break
            except requests.exceptions.Timeout:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"Request timed out. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    return FunctionResultStatus.FAILED, "API request timed out after multiple attempts", {
                        "contract_address": contract_address,
                        "platform_id": platform_id,
                        "chain_id": chain_id,
                        "error": "Request timeout"
                    }
            except requests.exceptions.RequestException as e:
                return FunctionResultStatus.FAILED, f"API request error: {str(e)}", {
                    "contract_address": contract_address,
                    "platform_id": platform_id,
                    "chain_id": chain_id,
                    "error": str(e)
                }
        
        # Process the response
        if response.status_code == 200:
            scan_results = response.json()
            
            # Extract data from the response
            scan_report = scan_results.get("scan_report", {})
            scan_summary = scan_report.get("scan_summary", {})
            
            # Extract issue counts
            issue_severity = scan_summary.get("issue_severity_distribution", {})
            critical_count = issue_severity.get("critical", 0)
            high_count = issue_severity.get("high", 0)
            medium_count = issue_severity.get("medium", 0)
            low_count = issue_severity.get("low", 0)
            gas_count = issue_severity.get("gas", 0)
            info_count = issue_severity.get("informational", 0)
            
            # Total vulnerabilities
            vulnerabilities_count = critical_count + high_count + medium_count + low_count
            
            # Prepare result info
            result_info = {
                "contract_address": contract_address,
                "platform_id": platform_id,
                "chain_id": chain_id,
                "platform_name": platform_name,
                "chain_name": chain_name,
                "vulnerabilities_count": vulnerabilities_count,
                "security_risk_count": critical_count + high_count + medium_count,
                "optimization_count": gas_count,
                "informational_count": info_count,
                "low_risk_count": low_count,
                "risk_level": scan_summary.get("threat_scan_risk_level", "Unknown"),
                "score": scan_summary.get("score_v2", ""),
                "score_rating": scan_summary.get("score_rating", "Unknown"),
                "scan_url": scan_report.get("scanner_reference_url", ""),
                # New fields
                "contract_name": scan_report.get("contractname", "Unknown"),
                "contract_url": scan_report.get("contract_url", ""),
                "is_quick_scan": scan_report.get("is_quick_scan", False),
                "is_verified_scan": scan_report.get("is_verified_scan", False),
                "scan_type": scan_report.get("request_type", "Unknown"),
                "total_detectors_count": scan_results.get("total_detectors_count", 0),
                "lines_analyzed": scan_summary.get("lines_analyzed_count", 0),
                "scan_time": scan_summary.get("scan_time_taken", 0),
                "scan_results": scan_results,
                "scan_api_version": "v1"
            }
            
            return FunctionResultStatus.DONE, f"Successfully scanned contract {contract_address} on {platform_name} ({chain_name}).", result_info
        else:
            return FunctionResultStatus.FAILED, f"API request failed with status code {response.status_code}", {
                "contract_address": contract_address,
                "platform_id": platform_id,
                "chain_id": chain_id,
                "error": response.text[:1000] if response.text else "Unknown error"
            }
    
    except Exception as e:
        print(f"Error scanning contract: {str(e)}")
        traceback.print_exc()
        return FunctionResultStatus.FAILED, f"Error scanning contract: {str(e)}", {
            "contract_address": contract_address,
            "platform_id": platform_id,
            "chain_id": chain_id,
            "error": str(e)
        }

def threat_scan(platform_id: str, chain_id: str, contract_address: str) -> Tuple[FunctionResultStatus, str, dict]:
    """
    Function to perform a threat scan on a smart contract.
    Uses the v2 API endpoint for threat scanning.
    
    Note: This API can return either an initialization response or a complete scan result.
    If it returns an initialization response, the actual scan results will be pushed to configured endpoints
    or need to be retrieved separately.
    """
    if not all([platform_id, chain_id, contract_address]):
        return FunctionResultStatus.FAILED, "Missing required parameters", {}
    
    # Validate contract address format
    if not contract_address.startswith("0x"):
        return FunctionResultStatus.FAILED, "Invalid contract address format. Address must start with '0x'", {}
    
    try:
        # Get platform and chain info
        info = get_platform_chain_info(platform_id, chain_id)
        
        platform_name = info.get("platform", {}).get("name", "Unknown Platform")
        chain_name = info.get("chain", {}).get("name", "Unknown Chain")
        
        # Construct the API URL for threat scan (v2 API)
        api_url = f"https://api.solidityscan.com/api/v2/threatscan/{platform_id}/{chain_id}/{contract_address}"
        
        print(f"Making API request to: {api_url}")
        
        # Set up headers with API key
        headers = {
            "Authorization": f"Token {solidityscan_api_key}",
            "Content-Type": "application/json"
        }
        
        # Make the API request with retry logic
        max_retries = 3
        retry_count = 0
        retry_delay = 5  # seconds
        
        while retry_count < max_retries:
            try:
                response = requests.get(api_url, headers=headers, timeout=60)
                break
            except requests.exceptions.Timeout:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"Request timed out. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    return FunctionResultStatus.FAILED, "API request timed out after multiple attempts", {
                        "contract_address": contract_address,
                        "platform_id": platform_id,
                        "chain_id": chain_id,
                        "error": "Request timeout"
                    }
            except requests.exceptions.RequestException as e:
                return FunctionResultStatus.FAILED, f"API request error: {str(e)}", {
                    "contract_address": contract_address,
                    "platform_id": platform_id,
                    "chain_id": chain_id,
                    "error": str(e)
                }
        
        # Process the response
        if response.status_code == 200:
            scan_results = response.json()
            
            # Check if this is an initialization response or a complete scan result
            if "scan_id" in scan_results and "data" in scan_results and scan_results.get("scan_status") == "initialised":
                # This is an initialization response
                scan_id = scan_results.get("scan_id", "Unknown")
                scan_status = scan_results.get("scan_status", "Unknown")
                request_uuid = scan_results.get("request_uuid", "Unknown")
                total_detectors_count = scan_results.get("total_detectors_count", 0)
                status = scan_results.get("status", "Unknown")
                
                # Prepare result info for initialization response
                result_info = {
                    "contract_address": contract_address,
                    "platform_id": platform_id,
                    "chain_id": chain_id,
                    "platform_name": platform_name,
                    "chain_name": chain_name,
                    "scan_id": scan_id,
                    "scan_status": scan_status,
                    "request_uuid": request_uuid,
                    "total_detectors_count": total_detectors_count,
                    "status": status,
                    "contract_platform": scan_results.get("contract_platform", "Unknown"),
                    "contract_chain": scan_results.get("contract_chain", "Unknown"),
                    "scan_results": scan_results,
                    "scan_api_version": "v2",
                    "is_initialization": True
                }
                
                # Check if the scan was successfully initialized
                if status == "success" and scan_status == "initialised":
                    return FunctionResultStatus.DONE, f"Successfully initiated threat scan on contract {contract_address} on {platform_name} ({chain_name}). Scan ID: {scan_id}", result_info
                else:
                    return FunctionResultStatus.FAILED, f"Threat scan initialization failed with status: {status}", result_info
            else:
                # This is a complete scan result
                scan_report = scan_results.get("scan_report", {})
                total_detectors_count = scan_results.get("total_detectors_count", 0)
                status = scan_results.get("status", "Unknown")
                
                # Extract threat scan details
                threat_scan_details = scan_report.get("threat_scan_details", [])
                ts_scan_details = scan_report.get("ts_scan_details", [])
                threat_score = scan_report.get("threat_score", "Unknown")
                ts_scan_status = scan_report.get("ts_scan_status", "Unknown")
                
                # Count issues by severity
                severity_counts = {
                    "Beneficial": 0,
                    "No Impact": 0,
                    "Low Risk": 0,
                    "Moderate Risk": 0,
                    "High Risk": 0,
                    "Unavailable": 0
                }
                
                # Count pass/fail issues
                pass_count = 0
                fail_count = 0
                skipped_count = 0
                
                # Process threat scan details
                for issue in threat_scan_details:
                    severity = issue.get("issue_severity", "Unknown")
                    issue_status = issue.get("issue_status", "Unknown")
                    
                    if severity in severity_counts:
                        severity_counts[severity] += 1
                    
                    if issue_status == "pass":
                        pass_count += 1
                    elif issue_status == "fail":
                        fail_count += 1
                    elif issue_status == "skipped":
                        skipped_count += 1
                
                # Process transaction simulation details
                for issue in ts_scan_details:
                    issue_status = issue.get("issue_status", "Unknown")
                    
                    if issue_status == "pass":
                        pass_count += 1
                    elif issue_status == "fail":
                        fail_count += 1
                    elif issue_status == "skipped":
                        skipped_count += 1
                
                # Prepare result info for complete scan result
                result_info = {
                    "contract_address": contract_address,
                    "platform_id": platform_id,
                    "chain_id": chain_id,
                    "platform_name": platform_name,
                    "chain_name": chain_name,
                    "contract_name": scan_report.get("contractname", "Unknown"),
                    "contract_url": scan_report.get("contract_url", ""),
                    "threat_score": threat_score,
                    "ts_scan_status": ts_scan_status,
                    "total_detectors_count": total_detectors_count,
                    "severity_counts": severity_counts,
                    "pass_count": pass_count,
                    "fail_count": fail_count,
                    "skipped_count": skipped_count,
                    "scan_url": scan_report.get("scanner_reference_url", ""),
                    "scan_results": scan_results,
                    "scan_api_version": "v2",
                    "is_initialization": False
                }
                
                # Check if the scan was successful - just check if status is success
                if status == "success":
                    return FunctionResultStatus.DONE, f"Successfully completed threat scan on contract {contract_address} on {platform_name} ({chain_name}). Threat Score: {threat_score}", result_info
                else:
                    return FunctionResultStatus.FAILED, f"Threat scan failed with status: {status}", result_info
        else:
            return FunctionResultStatus.FAILED, f"API request failed with status code {response.status_code}", {
                "contract_address": contract_address,
                "platform_id": platform_id,
                "chain_id": chain_id,
                "error": response.text[:1000] if response.text else "Unknown error"
            }
    
    except Exception as e:
        print(f"Error scanning contract: {str(e)}")
        traceback.print_exc()
        return FunctionResultStatus.FAILED, f"Error scanning contract: {str(e)}", {
            "contract_address": contract_address,
            "platform_id": platform_id,
            "chain_id": chain_id,
            "error": str(e)
        }

def vulnerability_and_threat_scan(platform_id: str, chain_id: str, contract_address: str) -> Tuple[FunctionResultStatus, str, dict]:
    """
    Function to perform both vulnerability and threat scans on a smart contract.
    This function combines the results of both scans into a single result.
    """
    print(f"Starting combined vulnerability and threat scan for contract {contract_address} on platform {platform_id}, chain {chain_id}")
    
    # First, perform the vulnerability scan
    vuln_status, vuln_message, vuln_info = vulnerability_scan(platform_id, chain_id, contract_address)
    
    # If vulnerability scan failed, return the failure
    if vuln_status == FunctionResultStatus.FAILED:
        return vuln_status, f"Vulnerability scan failed: {vuln_message}", vuln_info
    
    print("Vulnerability scan completed successfully. Starting threat scan...")
    
    # Next, perform the threat scan
    threat_status, threat_message, threat_info = threat_scan(platform_id, chain_id, contract_address)
    
    # If both scans succeeded, combine the results
    if threat_status == FunctionResultStatus.DONE:
        # Combine the results from both scans
        combined_info = {
            # Basic contract info
            "contract_address": contract_address,
            "platform_id": platform_id,
            "chain_id": chain_id,
            "platform_name": vuln_info.get("platform_name"),
            "chain_name": vuln_info.get("chain_name"),
            "contract_name": vuln_info.get("contract_name"),
            "contract_url": vuln_info.get("contract_url"),
            
            # Vulnerability scan results
            "vulnerabilities_count": vuln_info.get("vulnerabilities_count"),
            "security_risk_count": vuln_info.get("security_risk_count"),
            "optimization_count": vuln_info.get("optimization_count"),
            "informational_count": vuln_info.get("informational_count"),
            "low_risk_count": vuln_info.get("low_risk_count"),
            "vulnerability_score": vuln_info.get("score"),
            "vulnerability_score_rating": vuln_info.get("score_rating"),
            "vulnerability_scan_url": vuln_info.get("scan_url"),
            "vulnerability_scan_results": vuln_info.get("scan_results"),
            
            # Threat scan results
            "threat_score": threat_info.get("threat_score"),
            "ts_scan_status": threat_info.get("ts_scan_status"),
            "severity_counts": threat_info.get("severity_counts"),
            "pass_count": threat_info.get("pass_count"),
            "fail_count": threat_info.get("fail_count"),
            "skipped_count": threat_info.get("skipped_count"),
            "threat_scan_url": threat_info.get("scan_url"),
            "threat_scan_results": threat_info.get("scan_results"),
            
            # Combined scan info
            "both_scans_successful": True
        }
        
        return FunctionResultStatus.DONE, f"Successfully completed both vulnerability and threat scans for contract {contract_address}", combined_info
    else:
        # If threat scan failed but vulnerability scan succeeded, return vulnerability results with a note
        vuln_info["threat_scan_status"] = FunctionResultStatus.FAILED
        vuln_info["threat_scan_message"] = threat_message
        vuln_info["both_scans_successful"] = False
        
        return FunctionResultStatus.DONE, f"Vulnerability scan succeeded but threat scan failed: {threat_message}", vuln_info

#######################
# Main Function
#######################

def main():
    """
    Main function to run the standalone scanner.
    """
    print("\nStandalone Smart Contract Scanner")
    print("================================")
    
    # Check if API key is set
    if not solidityscan_api_key:
        print("Error: SOLIDITYSCAN_API_KEY environment variable not set")
        print("Please set it with: export SOLIDITYSCAN_API_KEY=your_api_key_here")
        return
    
    print(f"Using SolidityScan API Key: {solidityscan_api_key[:4]}...{solidityscan_api_key[-4:] if len(solidityscan_api_key) > 8 else ''}")
    
    # Loop to allow multiple scans
    while True:
        # Step 0: Choose scan type
        print("\nStep 0: Select scan type")
        print("1. Vulnerability Scan (v1 API)")
        print("2. Threat Scan (v2 API)")
        print("3. Combined Scan (Both)")
        print("4. Exit")
        
        scan_type_choice = input("\nEnter scan type (1-4): ")
        
        if scan_type_choice == "4":
            print("Exiting...")
            break
        
        scan_type = "vulnerability" if scan_type_choice == "1" else "threat" if scan_type_choice == "2" else "combined"
        
        print(f"Selected Scan Type: {scan_type.capitalize()} Scan")
        
        # Step 1: Get platform ID
        print("\nStep 1: Select a platform")
        print("Available Platforms:")
        platforms, _ = get_platforms_and_chains()
        for platform in platforms:  # Show ALL platforms
            print(f"- {platform['name']} (ID: {platform['id']})")
        
        platform_id = input("\nEnter Platform ID: ")
        
        # Find platform name
        platform_name = "Unknown Platform"
        for platform in platforms:
            if platform["id"] == platform_id:
                platform_name = platform["name"]
                break
        
        print(f"Selected Platform: {platform_name} (ID: {platform_id})")
        
        # Step 2: Get chain ID
        print("\nStep 2: Select a chain")
        print("Available Chains for this platform:")
        _, chains = get_platforms_and_chains()
        platform_chains = [chain for chain in chains if chain["platform_id"] == platform_id]
        if platform_chains:
            for chain in platform_chains:  # Show ALL chains for the platform
                print(f"- {chain['name']} (ID: {chain['id']})")
        else:
            print("- mainnet (ID: 1)")
            print("- testnet (ID: 2)")
        
        chain_id = input("\nEnter Chain ID: ")
        
        # Find chain name
        chain_name = "Unknown Chain"
        for chain in chains:
            if chain["platform_id"] == platform_id and chain["id"] == chain_id:
                chain_name = chain["name"]
                break
        
        print(f"Selected Chain: {chain_name} (ID: {chain_id})")
        
        # Step 3: Get contract address
        print("\nStep 3: Enter contract address")
        contract_address = input("Enter Contract Address (must start with 0x): ")
        
        if not contract_address.startswith("0x"):
            print("Error: Invalid contract address format. Address must start with '0x'")
            continue
        
        # Confirm the scan
        print(f"\nPerforming {scan_type} scan on contract {contract_address} on {platform_name} (Platform ID: {platform_id}, Chain ID: {chain_id})...")
        
        # Call the appropriate scan function based on scan type
        if scan_type == "vulnerability":
            status, message, info = vulnerability_scan(platform_id, chain_id, contract_address)
        elif scan_type == "threat":
            status, message, info = threat_scan(platform_id, chain_id, contract_address)
        else:  # combined scan
            status, message, info = vulnerability_and_threat_scan(platform_id, chain_id, contract_address)
        
        # Display results
        print(f"\nScan Status: {status}")
        print(f"Message: {message}")
        
        if status == FunctionResultStatus.DONE:
            print("\nScan Results:")
            
            if scan_type == "vulnerability":
                # Display vulnerability scan results (v1 API)
                print(f"- Contract Name: {info.get('contract_name', 'Unknown')}")
                print(f"- Risk Level: {info.get('risk_level', 'Unknown')}")
                print(f"- Score: {info.get('score', 'Unknown')} ({info.get('score_rating', 'Unknown')})")
                print(f"- Total Vulnerabilities: {info.get('vulnerabilities_count', 0)}")
                print(f"  - Critical: {info.get('scan_results', {}).get('scan_report', {}).get('scan_summary', {}).get('issue_severity_distribution', {}).get('critical', 0)}")
                print(f"  - High: {info.get('scan_results', {}).get('scan_report', {}).get('scan_summary', {}).get('issue_severity_distribution', {}).get('high', 0)}")
                print(f"  - Medium: {info.get('scan_results', {}).get('scan_report', {}).get('scan_summary', {}).get('issue_severity_distribution', {}).get('medium', 0)}")
                print(f"  - Low: {info.get('scan_results', {}).get('scan_report', {}).get('scan_summary', {}).get('issue_severity_distribution', {}).get('low', 0)}")
                print(f"- Security Risks: {info.get('security_risk_count', 0)}")
                print(f"- Optimization Opportunities: {info.get('optimization_count', 0)}")
                print(f"- Informational Issues: {info.get('informational_count', 0)}")
                
                if info.get('scan_url'):
                    print(f"\nDetailed scan results available at: {info.get('scan_url')}")
            
            elif scan_type == "threat":
                if info.get('is_initialization', False):
                    # Display threat scan initialization results (v2 API)
                    print(f"- Scan ID: {info.get('scan_id', 'Unknown')}")
                    print(f"- Scan Status: {info.get('scan_status', 'Unknown')}")
                    print(f"- Request UUID: {info.get('request_uuid', 'Unknown')}")
                    print(f"- Contract Platform: {info.get('contract_platform', 'Unknown')}")
                    print(f"- Contract Chain: {info.get('contract_chain', 'Unknown')}")
                    print(f"- Total Detectors: {info.get('total_detectors_count', 0)}")
                    print(f"- Status: {info.get('status', 'Unknown')}")
                    print("\nNote: The threat scan is asynchronous. Results will be pushed to configured endpoints.")
                else:
                    # Display complete threat scan results (v2 API)
                    print(f"- Contract Name: {info.get('contract_name', 'Unknown')}")
                    print(f"- Threat Score: {info.get('threat_score', 'Unknown')}")
                    print(f"- Scan Status: {info.get('ts_scan_status', 'Unknown')}")
                    
                    # Display severity counts
                    severity_counts = info.get('severity_counts', {})
                    print("\nIssues by Severity:")
                    for severity, count in severity_counts.items():
                        print(f"- {severity}: {count}")
                    
                    # Display pass/fail counts
                    print(f"\nIssue Status:")
                    print(f"- Pass: {info.get('pass_count', 0)}")
                    print(f"- Fail: {info.get('fail_count', 0)}")
                    print(f"- Skipped: {info.get('skipped_count', 0)}")
                    
                    if info.get('scan_url'):
                        print(f"\nDetailed scan results available at: {info.get('scan_url')}")
            
            else:  # combined scan
                # Display combined scan results
                print(f"- Contract Name: {info.get('contract_name', 'Unknown')}")
                print(f"- Both Scans Successful: {info.get('both_scans_successful', False)}")
                
                print("\nVulnerability Scan Results:")
                print(f"- Score: {info.get('vulnerability_score', 'Unknown')} ({info.get('vulnerability_score_rating', 'Unknown')})")
                print(f"- Total Vulnerabilities: {info.get('vulnerabilities_count', 0)}")
                print(f"- Security Risks: {info.get('security_risk_count', 0)}")
                print(f"- Optimization Opportunities: {info.get('optimization_count', 0)}")
                print(f"- Informational Issues: {info.get('informational_count', 0)}")
                
                if info.get('both_scans_successful', False):
                    print("\nThreat Scan Results:")
                    print(f"- Threat Score: {info.get('threat_score', 'Unknown')}")
                    
                    # Display severity counts
                    severity_counts = info.get('severity_counts', {})
                    print("\nIssues by Severity:")
                    for severity, count in severity_counts.items():
                        print(f"- {severity}: {count}")
                    
                    # Display pass/fail counts
                    print(f"\nIssue Status:")
                    print(f"- Pass: {info.get('pass_count', 0)}")
                    print(f"- Fail: {info.get('fail_count', 0)}")
                    print(f"- Skipped: {info.get('skipped_count', 0)}")
                else:
                    print("\nThreat Scan Failed:")
                    print(f"- Message: {info.get('threat_scan_message', 'Unknown error')}")
                
                if info.get('vulnerability_scan_url'):
                    print(f"\nVulnerability scan results available at: {info.get('vulnerability_scan_url')}")
                
                if info.get('both_scans_successful', False) and info.get('threat_scan_url'):
                    print(f"Threat scan results available at: {info.get('threat_scan_url')}")
        else:
            print("\nScan failed. Please check the error messages above.")
        
        # Ask if the user wants to see the full JSON response
        show_full = input("\nDo you want to see the full JSON response? (yes/no): ")
        if show_full.lower() in ['yes', 'y']:
            print("\nFull JSON Response:")
            if scan_type == "vulnerability":
                print(json.dumps(info.get('scan_results', {}), indent=2))
            elif scan_type == "threat":
                print(json.dumps(info.get('scan_results', {}), indent=2))
            else:  # combined scan
                print("\nVulnerability Scan Results:")
                print(json.dumps(info.get('vulnerability_scan_results', {}), indent=2))
                if info.get('both_scans_successful', False):
                    print("\nThreat Scan Results:")
                    print(json.dumps(info.get('threat_scan_results', {}), indent=2))
        
        # Ask if the user wants to scan another contract
        another = input("\nDo you want to scan another contract? (yes/no): ")
        if another.lower() not in ['yes', 'y']:
            print("Exiting...")
            break

if __name__ == "__main__":
    main()

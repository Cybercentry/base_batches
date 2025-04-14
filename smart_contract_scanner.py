"""
Smart Contract Scanner with two modes:
1. Direct API Test - Tests the SolidityScan APIs directly
2. Agent - Uses the Agent with the Worker, to conduct smart contract vulnerability and threat scans, on asking for parameters individually
"""

from game_sdk.game.agent import Agent, WorkerConfig
from game_sdk.game.custom_types import Function, Argument, FunctionResult, FunctionResultStatus
from typing import Tuple, List, Dict
import os
import requests
import json
import time
import traceback
import re

# Get API key from environment variables
game_api_key = os.environ.get("GAME_API_KEY")
solidityscan_api_key = os.environ.get("SOLIDITYSCAN_API_KEY")

#######################
# Shared Functions
#######################

def get_worker_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    """
    State management function for the smart contract scanner worker.
    """
    # Initialize state if it doesn't exist
    if current_state is None:
        new_state = {
            "scanned_contracts": [],
            # Complete list of all platforms from SolidityScan's platform parameters
            "platforms": [
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
            ],
            # Comprehensive list of chains for all platforms based on provided data
            "chains": [
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
                {"platform_id": "16", "id": "10", "name": "Neno Mainnet"},
                {"platform_id": "16", "id": "11", "name": "Neon Devnet"},
                {"platform_id": "16", "id": "12", "name": "Gnosis Mainnet"},
                {"platform_id": "16", "id": "13", "name": "Gnosis Chiado"},
                {"platform_id": "16", "id": "14", "name": "OP Mainnet"},
                {"platform_id": "16", "id": "15", "name": "OP Goerli"},
                {"platform_id": "16", "id": "16", "name": "OP Sepolia"},
                {"platform_id": "16", "id": "17", "name": "Rootstock Mainnet"},
                {"platform_id": "16", "id": "18", "name": "Immutable Testnet"},
                {"platform_id": "16", "id": "19", "name": "Era Mainnet"},
                {"platform_id": "16", "id": "20", "name": "fuse-mainnet"},
                {"platform_id": "16", "id": "21", "name": "fuse-testnet"},
                {"platform_id": "16", "id": "22", "name": "shimmer-mainnet"},
                {"platform_id": "16", "id": "23", "name": "shimmer-testnet"},
                {"platform_id": "16", "id": "24", "name": "lightlink-mainnet"},
                {"platform_id": "16", "id": "25", "name": "lightlink-testnet"},
                {"platform_id": "16", "id": "26", "name": "shibariumscan-mainnet"},
                {"platform_id": "16", "id": "27", "name": "shibariumscan-testnet"},
                {"platform_id": "16", "id": "28", "name": "Rootstock Testnet"},
                {"platform_id": "16", "id": "29", "name": "Immutable Mainnet"},
                {"platform_id": "16", "id": "30", "name": "Zetachain Mainnet"},
                {"platform_id": "16", "id": "31", "name": "Zetachain Testnet"},
                {"platform_id": "16", "id": "32", "name": "Celo Alfajores Testnet"},
                {"platform_id": "16", "id": "33", "name": "Celo Baklava Testnet"},
                {"platform_id": "16", "id": "34", "name": "Polygon Zkevm Mainnet"},
                {"platform_id": "16", "id": "35", "name": "Creditcoin Testnet"},
                {"platform_id": "16", "id": "36", "name": "Stability Mainnet"},
                {"platform_id": "16", "id": "37", "name": "Stability Testnet"},
                {"platform_id": "16", "id": "38", "name": "Iota EVM Mainnet"},
                {"platform_id": "16", "id": "39", "name": "Iota EVM Testnet"},
                {"platform_id": "16", "id": "40", "name": "Astar Mainnet"},
                {"platform_id": "16", "id": "41", "name": "Astar Shibuya Testnet"},
                {"platform_id": "16", "id": "42", "name": "Astar Shiden Testnet"},
                {"platform_id": "16", "id": "43", "name": "Astar Zkyoto Testnet"},
                {"platform_id": "16", "id": "44", "name": "Astar Zkevm Mainnet"},
                {"platform_id": "16", "id": "45", "name": "Tangible Unreal Testnet"},
                {"platform_id": "16", "id": "46", "name": "Tangible Real Mainnet"},
                {"platform_id": "16", "id": "47", "name": "Lisk Testnet"},
                {"platform_id": "16", "id": "48", "name": "Reya Mainnet"},
                {"platform_id": "16", "id": "49", "name": "Reya Cronos Testnet"},
                {"platform_id": "16", "id": "50", "name": "Playance Mainnet"},
                {"platform_id": "16", "id": "51", "name": "Playance Playblock Testnet"},
                {"platform_id": "16", "id": "52", "name": "Verify Testnet"},
                {"platform_id": "16", "id": "53", "name": "Lukso Mainnet"},
                {"platform_id": "16", "id": "54", "name": "Omni Testnet"},
                {"platform_id": "16", "id": "55", "name": "Blackfort Mainnet"},
                {"platform_id": "16", "id": "56", "name": "Blackfort Testnet"},
                {"platform_id": "16", "id": "57", "name": "Arbitrum One Mainnet"},
                {"platform_id": "16", "id": "58", "name": "Redstone Mainnet"},
                {"platform_id": "16", "id": "59", "name": "Redstone Garnet Testnet"},
                {"platform_id": "16", "id": "60", "name": "Connext Sepolia Testnet"},
                {"platform_id": "16", "id": "61", "name": "Anomaly Sepolia Testnet"},
                {"platform_id": "16", "id": "62", "name": "Zksync Mainnet"},
                {"platform_id": "16", "id": "63", "name": "Zksync Testnet"},
                {"platform_id": "16", "id": "64", "name": "Lineascan Testnet"},
                {"platform_id": "16", "id": "65", "name": "Lineascan Goerli Testnet"},
                {"platform_id": "16", "id": "66", "name": "Lineascan Sepolia Testnet"},
                {"platform_id": "16", "id": "69", "name": "AssetChain Testnet"},
                {"platform_id": "16", "id": "70", "name": "AssetChain Mainnet"},
                {"platform_id": "16", "id": "72", "name": "caminoscan-mainnet"},
                {"platform_id": "16", "id": "73", "name": "columbus-caminoscan-testnet"},
                {"platform_id": "16", "id": "74", "name": "etherlink-mainnet"},
                {"platform_id": "16", "id": "75", "name": "etherlink-testnet"},
                {"platform_id": "16", "id": "76", "name": "japanopenchain-testnet"},
                {"platform_id": "16", "id": "77", "name": "hemi-testnet"},
                {"platform_id": "16", "id": "78", "name": "soneium-mainnet"},
                {"platform_id": "16", "id": "79", "name": "soneium-minato-testnet"},
                
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
            ],
            # Add conversation state to track where we are in the parameter gathering process
            "conversation_state": {
                "awaiting_scan_request": True,  # Initially waiting for user to request a scan
                "awaiting_platform_id": False,
                "awaiting_chain_id": False,
                "awaiting_contract_address": False,
                "platform_id": None,
                "chain_id": None,
                "contract_address": None
            }
        }
    else:
        new_state = current_state
        
    return new_state

def get_platform_chain_info(state, platform_id=None, chain_id=None):
    """Helper function to get platform and chain information."""
    result = {}
    
    # Look up platform info
    if platform_id:
        for platform in state.get("platforms", []):
            if platform["id"] == platform_id:
                result["platform"] = platform
                break
    
    # Look up chain info
    if platform_id and chain_id:
        for chain in state.get("chains", []):
            if chain["platform_id"] == platform_id and chain["id"] == chain_id:
                result["chain"] = chain
                break
    
    return result

def vulnerability_scan(platform_id: str, chain_id: str, contract_address: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
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
        state = get_worker_state_fn(None, None)
        info = get_platform_chain_info(state, platform_id, chain_id)
        
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

def threat_scan(platform_id: str, chain_id: str, contract_address: str, **kwargs) -> Tuple[FunctionResultStatus, str, dict]:
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
        state = get_worker_state_fn(None, None)
        info = get_platform_chain_info(state, platform_id, chain_id)
        
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

# Create the vulnerability scan function
vulnerability_scan_fn = Function(
    fn_name="vulnerability_scan", 
    fn_description="Scan a smart contract for vulnerabilities, security risks, and optimization opportunities", 
    args=[
        Argument(
            name="platform_id", 
            type="string", 
            description="The identifier for the platform (e.g., \"17\" for basescan.org)"
        ),
        Argument(
            name="chain_id", 
            type="string", 
            description="The identifier of the blockchain network (e.g., \"1\" for mainnet)"
        ),
        Argument(
            name="contract_address", 
            type="string", 
            description="The hexadecimal address of the smart contract"
        )
    ],
    executable=vulnerability_scan
)

# Create the threat scan function
threat_scan_fn = Function(
    fn_name="threat_scan", 
    fn_description="Perform a threat scan on a smart contract to identify security threats. Note: This is an asynchronous API that initializes a scan and returns a scan ID.", 
    args=[
        Argument(
            name="platform_id", 
            type="string", 
            description="The identifier for the platform (e.g., \"17\" for basescan.org)"
        ),
        Argument(
            name="chain_id", 
            type="string", 
            description="The identifier of the blockchain network (e.g., \"1\" for mainnet)"
        ),
        Argument(
            name="contract_address", 
            type="string", 
            description="The hexadecimal address of the smart contract"
        )
    ],
    executable=threat_scan
)

#######################
# Agent Configuration
#######################

def get_agent_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    """
    State management function for the main agent.
    """
    if current_state is None:
        new_state = {
            "total_scans": 0,
            "successful_scans": 0,
            "failed_scans": 0,
            "last_scan_timestamp": None,
            "conversation_history": [],  # Add conversation history
            # Add conversation state to track where we are in the parameter gathering process
            "conversation_state": {
                "awaiting_scan_request": True,  # Initially waiting for user to request a scan
                "awaiting_scan_type": False,    # Added to choose between vulnerability and threat scan
                "awaiting_platform_id": False,
                "awaiting_chain_id": False,
                "awaiting_contract_address": False,
                "scan_type": None,              # Added to store the scan type
                "platform_id": None,
                "chain_id": None,
                "contract_address": None
            }
        }
    else:
        new_state = current_state
        
        # Update scan statistics if a scan was performed
        if function_result and hasattr(function_result, 'fn_name') and (function_result.fn_name == "vulnerability_scan" or function_result.fn_name == "threat_scan"):
            new_state["total_scans"] += 1
            
            if hasattr(function_result, 'status') and function_result.status == FunctionResultStatus.DONE:
                new_state["successful_scans"] += 1
                new_state["last_scan_timestamp"] = "now"  # You could add a timestamp here
                
                # Reset conversation state after successful scan
                if "conversation_state" in new_state:
                    new_state["conversation_state"] = {
                        "awaiting_scan_request": True,
                        "awaiting_scan_type": False,
                        "awaiting_platform_id": False,
                        "awaiting_chain_id": False,
                        "awaiting_contract_address": False,
                        "scan_type": None,
                        "platform_id": None,
                        "chain_id": None,
                        "contract_address": None
                    }
            else:
                new_state["failed_scans"] += 1

    return new_state

# Create the worker configuration for the agent
contract_scanner_config = WorkerConfig(
    id="contract_scanner",
    worker_description="""
    A worker specialized in scanning smart contracts for vulnerabilities, security risks, and optimization opportunities.
    
    This worker can scan contracts on various blockchain platforms including basescan.org (platform ID 17).
    
    It supports two types of scans:
    1. Vulnerability Scan - Identifies vulnerabilities, security risks, and optimization opportunities
    2. Threat Scan - Performs a specialized threat analysis on the contract
    """,
    get_state_fn=get_worker_state_fn,
    action_space=[vulnerability_scan_fn, threat_scan_fn]
)

def create_agent():
    """Create and return the agent instance with error handling"""
    try:
        agent = Agent(
            api_key=game_api_key,
            name="SecurityScanner",
            agent_goal="Identify and report security vulnerabilities and threats in blockchain smart contracts.",
            agent_description="""
            I am a security expert specialized in analyzing smart contracts for vulnerabilities and threats.
            
            I can help you scan smart contracts on various blockchain platforms including:
            - etherscan.io (1)
            - bscscan.com (2)
            - polygonscan.com (3)
            - basescan.org (17) - Base network (mainnet: 1, testnet: 2)
            - and many others
            
            I offer two types of scans:
            1. Vulnerability Scan - Identifies vulnerabilities, security risks, and optimization opportunities
            2. Threat Scan - Performs a specialized threat analysis on the contract
            
            When asked to scan a smart contract, I will ask for the required information one parameter at a time:
            
            1. First, I will ask which type of scan you want to perform
            2. Then, I will ask for the platform ID (e.g., '17' for basescan.org)
            3. After receiving the platform ID, I will ask for the chain ID (e.g., '1' for mainnet)
            4. Finally, I will ask for the contract address
            
            I will not ask for all parameters at once, and I will wait for the user to provide each parameter before asking for the next one.
            """,
            get_agent_state_fn=get_agent_state_fn,
            workers=[contract_scanner_config],
            model_name="Llama-3.3-70B-Instruct"
        )
        return agent
    except Exception as e:
        print(f"Error creating agent: {str(e)}")
        traceback.print_exc()
        return None

#######################
# Testing Functions
#######################

def direct_api_test():
    """
    Test the SolidityScan API directly without using the Worker or Agent.
    This function allows the user to input parameters and see the raw API response.
    """
    print("\nSmart Contract Scanner - Direct API Test")
    print("=======================================")
    
    # Check if API key is set
    if not solidityscan_api_key:
        print("Error: SOLIDITYSCAN_API_KEY environment variable not set")
        print("Please set it with: set SOLIDITYSCAN_API_KEY=your_api_key_here")
        return
    
    print(f"Using SolidityScan API Key: {solidityscan_api_key[:4]}...{solidityscan_api_key[-4:] if len(solidityscan_api_key) > 8 else ''}")
    
    # Loop to allow multiple scans
    while True:
        # Step 0: Choose scan type
        print("\nStep 0: Select scan type")
        print("1. Vulnerability Scan (v1 API)")
        print("2. Threat Scan (v2 API)")
        
        scan_type_choice = input("\nEnter scan type (1 or 2): ")
        scan_type = "vulnerability" if scan_type_choice == "1" else "threat"
        
        print(f"Selected Scan Type: {scan_type.capitalize()} Scan")
        
        # Step 1: Get platform ID
        print("\nStep 1: Select a platform")
        print("Available Platforms:")
        state = get_worker_state_fn(None, None)
        for platform in state["platforms"]:  # Show ALL platforms
            print(f"- {platform['name']} (ID: {platform['id']})")
        
        platform_id = input("\nEnter Platform ID: ")
        
        # Find platform name
        platform_name = "Unknown Platform"
        for platform in state["platforms"]:
            if platform["id"] == platform_id:
                platform_name = platform["name"]
                break
        
        print(f"Selected Platform: {platform_name} (ID: {platform_id})")
        
        # Step 2: Get chain ID
        print("\nStep 2: Select a chain")
        print("Available Chains for this platform:")
        chains = [chain for chain in state["chains"] if chain["platform_id"] == platform_id]
        if chains:
            for chain in chains:  # Show ALL chains for the platform
                print(f"- {chain['name']} (ID: {chain['id']})")
        else:
            print("- mainnet (ID: 1)")
            print("- testnet (ID: 2)")
        
        chain_id = input("\nEnter Chain ID: ")
        
        # Find chain name
        chain_name = "Unknown Chain"
        for chain in state["chains"]:
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
        else:  # threat scan
            status, message, info = threat_scan(platform_id, chain_id, contract_address)
        
        # Display results
        print(f"\nScan Status: {status}")
        print(f"Message: {message}")
        
        if status == FunctionResultStatus.DONE:
            print("\nScan Results:")
            print(f"- API Version: {info.get('scan_api_version', 'Unknown')}")
            
            if info.get('scan_api_version') == "v2":
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
                    print(f"- API Status: {info.get('scan_results', {}).get('status', 'Unknown')}")
                    
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
            else:
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
                print(f"- Scan Type: {info.get('scan_type', 'Unknown')} (Quick Scan: {info.get('is_quick_scan', False)}, Verified: {info.get('is_verified_scan', False)})")
                print(f"- Total Detectors: {info.get('total_detectors_count', 0)}")
                print(f"- Lines Analyzed: {info.get('lines_analyzed', 0)}")
                print(f"- Scan Time: {info.get('scan_time', 0)} seconds")
                
                if info.get('contract_url'):
                    print(f"\nContract URL: {info.get('contract_url')}")
                
                if info.get('scan_url'):
                    print(f"Detailed scan results available at: {info.get('scan_url')}")
        else:
            print("\nScan failed. Please check the error messages above.")
        
        # Ask if the user wants to see the full JSON response
        show_full = input("\nDo you want to see the full JSON response? (yes/no): ")
        if show_full.lower() in ['yes', 'y']:
            print("\nFull JSON Response:")
            print(json.dumps(info.get('scan_results', {}), indent=2))
        
        # Instead of asking to scan another contract, just prompt to return to main menu
        input("\nPress Enter to return to the main menu...")
        print("\nReturning to main menu...")
        return  # Return to main() function

def test_agent():
    """Test the Agent with its Worker with improved error handling"""
    print("\nSmart Contract Scanner - Agent Test")
    print("=================================")
    
    # Check if API keys are set
    if not game_api_key:
        print("Error: GAME_API_KEY environment variable not set")
        return
    
    if not solidityscan_api_key:
        print("Error: SOLIDITYSCAN_API_KEY environment variable not set")
        return
    
    print(f"Using GAME API Key: {game_api_key[:4]}...{game_api_key[-4:] if len(game_api_key) > 8 else ''}")
    print(f"Using SolidityScan API Key: {solidityscan_api_key[:4]}...{solidityscan_api_key[-4:] if len(solidityscan_api_key) > 8 else ''}")
    
    # Create the agent
    print("\nCreating agent...")
    agent = create_agent()
    
    if not agent:
        print("Failed to create agent. Exiting.")
        return
    
    print("Agent created successfully.")
    
    # Compile the agent
    try:
        print("Compiling agent...")
        agent.compile()
        print("Agent compiled successfully.")
    except Exception as e:
        print(f"Error compiling agent: {str(e)}")
        traceback.print_exc()
        return
    
    # Reset the agent
    try:
        print("Resetting agent...")
        agent.reset()
        print("Agent reset successfully.")
    except Exception as e:
        print(f"Error resetting agent: {str(e)}")
        traceback.print_exc()
        # Continue anyway
    
    print("\nAgent is ready. You can now interact with it.")
    print("First, express your interest in conducting a smart contract scan.")
    print("Type 'exit' to quit the test.")
    
    # Initialize conversation state
    state = {
        "awaiting_scan_request": True,
        "awaiting_scan_type": False,
        "awaiting_platform_id": False,
        "awaiting_chain_id": False,
        "awaiting_contract_address": False,
        "scan_type": None,
        "platform_id": None,
        "chain_id": None,
        "contract_address": None
    }
    
    while True:
        # Get user input with "You:" prompt for the first input
        if state["awaiting_scan_request"]:
            user_input = input("\nYou: ")
        elif state["awaiting_scan_type"]:
            user_input = input("")  # No newline to match direct API test format
        elif state["awaiting_platform_id"]:
            user_input = input("")  # No newline to match direct API test format
        elif state["awaiting_chain_id"]:
            user_input = input("")  # No newline to match direct API test format
        elif state["awaiting_contract_address"]:
            user_input = input("")  # No newline to match direct API test format
        else:
            user_input = input("\n")
        
        if user_input.lower() == 'exit':
            break
        
        # Process the user input based on the current state
        if state["awaiting_scan_request"]:
            # Check if the user is requesting a scan
            if re.search(r'scan|audit|check|vulnerabilit|secur|contract|threat', user_input.lower()):
                # User has expressed interest in scanning a contract
                state["awaiting_scan_request"] = False
                state["awaiting_scan_type"] = True
                
                # Display scan type options
                print("\nStep 0: Select scan type")
                print("1. Vulnerability Scan (v1 API)")
                print("2. Threat Scan (v2 API)")
                
                print("\nEnter scan type (1 or 2): ", end="")
            else:
                print("\nAgent: I'm a smart contract security scanner. I can help you scan smart contracts for vulnerabilities, security risks, and optimization opportunities. I offer two types of scans: Vulnerability Scan and Threat Scan. Let me know if you'd like to conduct a smart contract scan.")
        
        elif state["awaiting_scan_type"]:
            # User should be providing a scan type
            scan_type_choice = user_input.strip()
            
            if scan_type_choice in ["1", "2"]:
                state["scan_type"] = "vulnerability" if scan_type_choice == "1" else "threat"
                state["awaiting_scan_type"] = False
                state["awaiting_platform_id"] = True
                
                print(f"Selected Scan Type: {state['scan_type'].capitalize()} Scan")
                
                # Display available platforms - EXACTLY like direct_api_test
                platforms_info = get_worker_state_fn(None, None)["platforms"]
                print("\nStep 1: Select a platform")
                print("Available Platforms:")
                for platform in platforms_info:
                    print(f"- {platform['name']} (ID: {platform['id']})")
                
                print("\nEnter Platform ID: ", end="")
            else:
                print("I couldn't recognize that scan type. Please enter 1 for Vulnerability Scan or 2 for Threat Scan.")
                print("\nEnter scan type (1 or 2): ", end="")
        
        elif state["awaiting_platform_id"]:
            # User should be providing a platform ID
            platform_id = user_input.strip()
            
            # Validate platform ID
            platforms_info = get_worker_state_fn(None, None)["platforms"]
            platform_valid = False
            platform_name = "Unknown Platform"
            
            for platform in platforms_info:
                if platform["id"] == platform_id:
                    platform_valid = True
                    platform_name = platform["name"]
                    break
            
            if platform_valid:
                state["platform_id"] = platform_id
                state["awaiting_platform_id"] = False
                state["awaiting_chain_id"] = True
                
                # Display available chains for this platform - EXACTLY like direct_api_test
                chains_info = get_worker_state_fn(None, None)["chains"]
                chains = [chain for chain in chains_info if chain["platform_id"] == platform_id]
                
                print(f"Selected Platform: {platform_name} (ID: {platform_id})")
                print("\nStep 2: Select a chain")
                print("Available Chains for this platform:")
                
                if chains:
                    for chain in chains:
                        print(f"- {chain['name']} (ID: {chain['id']})")
                else:
                    print("- mainnet (ID: 1)")
                    print("- testnet (ID: 2)")
                
                print("\nEnter Chain ID: ", end="")
            else:
                print("I couldn't recognize that platform ID. Please provide a valid Platform ID.")
                print("\nEnter Platform ID: ", end="")
        
        elif state["awaiting_chain_id"]:
            # User should be providing a chain ID
            chain_id = user_input.strip()
            
            # Validate chain ID
            chains_info = get_worker_state_fn(None, None)["chains"]
            chain_valid = False
            chain_name = "Unknown Chain"
            
            for chain in chains_info:
                if chain["platform_id"] == state["platform_id"] and chain["id"] == chain_id:
                    chain_valid = True
                    chain_name = chain["name"]
                    break
            
            if chain_valid or chain_id in ["1", "2"]:  # Accept common chain IDs even if not explicitly listed
                state["chain_id"] = chain_id
                state["awaiting_chain_id"] = False
                state["awaiting_contract_address"] = True
                
                if not chain_valid:
                    chain_name = "mainnet" if chain_id == "1" else "testnet" if chain_id == "2" else "Unknown Chain"
                
                print(f"Selected Chain: {chain_name} (ID: {chain_id})")
                print("\nStep 3: Enter contract address")
                print("Enter Contract Address (must start with 0x): ", end="")
            else:
                print("I couldn't recognize that chain ID. Please provide a valid Chain ID.")
                print("\nEnter Chain ID: ", end="")
        
        elif state["awaiting_contract_address"]:
            # User should be providing a contract address
            contract_address = user_input.strip()
            
            # Validate contract address
            if contract_address.startswith("0x"):
                state["contract_address"] = contract_address
                state["awaiting_contract_address"] = False
                
                # We have all the parameters, perform the scan
                platform_id = state["platform_id"]
                chain_id = state["chain_id"]
                scan_type = state["scan_type"]
                
                # Get platform and chain names for display
                platforms_info = get_worker_state_fn(None, None)["platforms"]
                chains_info = get_worker_state_fn(None, None)["chains"]
                
                platform_name = "Unknown Platform"
                for platform in platforms_info:
                    if platform["id"] == platform_id:
                        platform_name = platform["name"]
                        break
                
                chain_name = "Unknown Chain"
                for chain in chains_info:
                    if chain["platform_id"] == platform_id and chain["id"] == chain_id:
                        chain_name = chain["name"]
                        break
                
                if chain_name == "Unknown Chain":
                    chain_name = "mainnet" if chain_id == "1" else "testnet" if chain_id == "2" else "Unknown Chain"
                
                print(f"\nPerforming {scan_type} scan on contract {contract_address} on {platform_name} (Platform ID: {platform_id}, Chain ID: {chain_id})...")
                
                # Call the appropriate scan function based on scan type
                if scan_type == "vulnerability":
                    status, message, info = vulnerability_scan(platform_id, chain_id, contract_address)
                else:  # threat scan
                    status, message, info = threat_scan(platform_id, chain_id, contract_address)
                
                # Display results
                print(f"\nScan Status: {status}")
                print(f"Message: {message}")
                
                if status == FunctionResultStatus.DONE:
                    print("\nScan Results:")
                    print(f"- API Version: {info.get('scan_api_version', 'Unknown')}")
                    
                    if info.get('scan_api_version') == "v2":
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
                            print(f"- API Status: {info.get('scan_results', {}).get('status', 'Unknown')}")
                            
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
                    else:
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
                        print(f"- Scan Type: {info.get('scan_type', 'Unknown')} (Quick Scan: {info.get('is_quick_scan', False)}, Verified: {info.get('is_verified_scan', False)})")
                        print(f"- Total Detectors: {info.get('total_detectors_count', 0)}")
                        print(f"- Lines Analyzed: {info.get('lines_analyzed', 0)}")
                        print(f"- Scan Time: {info.get('scan_time', 0)} seconds")
                        
                        if info.get('contract_url'):
                            print(f"\nContract URL: {info.get('contract_url')}")
                        
                        if info.get('scan_url'):
                            print(f"Detailed scan results available at: {info.get('scan_url')}")
                    
                    # Ask if user wants to see the full JSON response
                    show_full = input("\nDo you want to see the full JSON response? (yes/no): ")
                    if show_full.lower() in ['yes', 'y']:
                        print("\nFull JSON Response:")
                        print(json.dumps(info.get('scan_results', {}), indent=2))
                    
                    input("\nPress Enter to return to the main menu...")
                    print("\nReturning to main menu...")
                    return  # Return to main() function
                else:
                    print("\nScan failed. Please check the error messages above.")
                    input("\nPress Enter to return to the main menu...")
                    print("\nReturning to main menu...")
                    return  # Return to main() function
                
                # Reset state for next scan
                state["awaiting_scan_request"] = False
                state["awaiting_scan_type"] = False
                state["awaiting_platform_id"] = False
                state["awaiting_chain_id"] = False
                state["awaiting_contract_address"] = False
            else:
                print("Error: Invalid contract address format. Address must start with '0x'")
                print("Enter Contract Address (must start with 0x): ", end="")
        
        else:
            print("\nReturning to main menu...")
            # Exit the function to go back to the main menu
            return

def main():
    """Main function to run the script."""
    while True:
        print("\nSmart Contract Scanner - Dual Test Suite")
        print("--------------------------------------")
        print("Select a mode:")
        print("1. Direct API Test (Test the SolidityScan APIs directly)")
        print("2. Agent (Use the Agent with the Worker)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            direct_api_test()
            # Continue the loop to show the menu again
        elif choice == "2":
            test_agent()
            # Continue the loop to show the menu again
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

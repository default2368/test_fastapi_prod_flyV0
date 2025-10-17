from fastapi import APIRouter
import requests
import json
import time
from datetime import datetime

router = APIRouter(prefix="/test", tags=["Claude Test"])

@router.get("/test-claude")
async def test_claude_configuration():
    """Testa il server MCP come farebbe Claude Desktop"""
    
    MCP_URL = "https://test-mcp-prodv1.fly.dev/sse"
    
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "mcp_server_url": MCP_URL,
        "tests": {}
    }
    
    # 1. Initialize (come fa Claude)
    initialize_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {"listChanged": True},
                "resources": {"subscribe": False, "listChanged": True},
                "prompts": {"listChanged": True},
                "tools": {"listChanged": True}
            },
            "clientInfo": {
                "name": "Claude-Desktop",
                "version": "1.0.0"
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    
    try:
        # Initialize request
        response = requests.post(MCP_URL, json=initialize_payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Parse SSE response
            initialize_data = None
            server_info = None
            lines = response.text.strip().split('\n')
            
            for line in lines:
                if line.startswith('data:'):
                    data = json.loads(line[5:])
                    initialize_data = data
                    
                    # Extract server info
                    server_info = data.get('result', {}).get('serverInfo', {})
                    # Try to extract sessionId if present (needed for subsequent calls)
                    session_id = data.get('result', {}).get('sessionId')
                    break
            
            test_results["tests"]["initialize"] = {
                "status": "success",
                "status_code": response.status_code,
                "server_info": server_info,
                "initialize_data": initialize_data,
                "session_id": session_id if 'session_id' in locals() else None
            }
        else:
            test_results["tests"]["initialize"] = {
                "status": "error",
                "status_code": response.status_code,
                "response_text": response.text
            }
        
        # 2. List tools (come farebbe Claude dopo initialize)
        time.sleep(0.5)  # Breve pausa tra le richieste
        
        tools_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        # If we extracted a session id from initialize, include it in params
        if 'session_id' in locals() and session_id:
            tools_payload["params"] = {"sessionId": session_id}
        
        tools_response = requests.post(MCP_URL, json=tools_payload, headers=headers, timeout=10)
        
        if tools_response.status_code == 200:
            tools_data = None
            available_tools = []
            lines = tools_response.text.strip().split('\n')
            
            for line in lines:
                if line.startswith('data:'):
                    tools_data = json.loads(line[5:])
                    tools = tools_data.get('result', {}).get('tools', [])
                    available_tools = [
                        {
                            "name": tool.get('name'),
                            "description": tool.get('description'),
                            "inputSchema": tool.get('inputSchema', {})
                        }
                        for tool in tools
                    ]
                    break
            
            test_results["tests"]["tools_list"] = {
                "status": "success",
                "status_code": tools_response.status_code,
                "tools_count": len(available_tools),
                "tools": available_tools,
                "tools_data": tools_data
            }
        else:
            test_results["tests"]["tools_list"] = {
                "status": "error",
                "status_code": tools_response.status_code,
                "response_text": tools_response.text
            }
        
        # Calcola riepilogo
        total_tests = len(test_results["tests"])
        successful_tests = sum(1 for test in test_results["tests"].values() if test["status"] == "success")
        
        test_results["summary"] = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": f"{(successful_tests/total_tests)*100:.1f}%",
            "claude_ready": successful_tests == total_tests
        }
        
        # Configurazione per Claude
        if test_results["summary"]["claude_ready"]:
            test_results["claude_configuration"] = {
                "mcpServers": {
                    "flymcp": {
                        "command": "npx",
                        "args": [
                            "@modelcontextprotocol/server-flymcp",
                            MCP_URL
                        ]
                    }
                }
            }
        
        return test_results
        
    except requests.exceptions.Timeout:
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "error": "Timeout nella connessione al server MCP",
            "mcp_server_url": MCP_URL
        }
    except requests.exceptions.ConnectionError:
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "error", 
            "error": "Impossibile connettersi al server MCP",
            "mcp_server_url": MCP_URL
        }
    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "error": f"Errore durante il test Claude: {str(e)}",
            "mcp_server_url": MCP_URL
        }

@router.get("/claude-config")
async def get_claude_config():
    """Restituisce la configurazione JSON per Claude Desktop"""
    
    MCP_URL = "https://test-mcp-prodv1.fly.dev/mcp"
    
    config = {
        "mcpServers": {
            "flymcp": {
                "command": "npx",
                "args": [
                    "@modelcontextprotocol/server-flymcp", 
                    MCP_URL
                ]
            }
        }
    }
    
    # Versione alternativa per HTTP diretto
    config_alternative = {
        "mcpServers": {
            "flymcp": {
                "url": MCP_URL
            }
        }
    }
    
    return {
        "timestamp": datetime.now().isoformat(),
        "mcp_server_url": MCP_URL,
        "configurations": {
            "recommended": {
                "description": "Configurazione con npx (raccomandata)",
                "config": config,
                "file_location": {
                    "macos": "~/Library/Application Support/Claude/claude_desktop_config.json",
                    "windows": "%APPDATA%\\Claude\\claude_desktop_config.json", 
                    "linux": "~/.config/Claude/claude_desktop_config.json"
                }
            },
            "alternative": {
                "description": "Configurazione HTTP diretta (alternativa)",
                "config": config_alternative
            }
        },
        "instructions": {
            "1": "Copia la configurazione desiderata",
            "2": "Incolla nel file di configurazione di Claude Desktop",
            "3": "Riavvia Claude Desktop",
            "4": "Verifica che i tools MCP siano disponibili"
        }
    }

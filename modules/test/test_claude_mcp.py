import requests
import json
import time

def test_mcp_for_claude():
    """Testa il server MCP come farebbe Claude"""
    
    MCP_URL = "https://test-mcp-prodv1.fly.dev/mcp"
    
    print("🧪 TEST MCP PER CLAUDE DESKTOP")
    print("=" * 50)
    
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
        print(f"✅ Initialize: {response.status_code}")
        
        if response.status_code == 200:
            # Parse SSE response
            lines = response.text.strip().split('\n')
            for line in lines:
                if line.startswith('data:'):
                    data = json.loads(line[5:])
                    print(f"📦 Initialize Result: {json.dumps(data, indent=2)}")
                    
                    # Extract server info
                    server_info = data.get('result', {}).get('serverInfo', {})
                    print(f"🎯 Server: {server_info.get('name')} v{server_info.get('version')}")
        
        # 2. List tools (come farebbe Claude dopo initialize)
        time.sleep(1)
        tools_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        tools_response = requests.post(MCP_URL, json=tools_payload, headers=headers, timeout=10)
        print(f"\n✅ Tools/List: {tools_response.status_code}")
        
        if tools_response.status_code == 200:
            lines = tools_response.text.strip().split('\n')
            for line in lines:
                if line.startswith('data:'):
                    tools_data = json.loads(line[5:])
                    tools = tools_data.get('result', {}).get('tools', [])
                    print(f"🔧 Tools disponibili: {len(tools)}")
                    for tool in tools:
                        print(f"   - {tool.get('name')}: {tool.get('description')}")
        
        print("\n🎉 SERVER MCP PRONTO PER CLAUDE!")
        print("📋 Configura Claude Desktop con:")
        print(f"   URL: {MCP_URL}")
        
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    test_mcp_for_claude()

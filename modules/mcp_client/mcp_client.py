import requests
import json
from datetime import datetime

class MCPClient:
    def __init__(self, mcp_server_url: str = "https://test-mcp-prodv1.fly.dev"):
        self.mcp_url = mcp_server_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
    
    def parse_sse_response(self, response_text: str) -> list:
        """Parsa una risposta SSE (Server-Sent Events)"""
        events = []
        lines = response_text.strip().split('\n')
        
        current_event = {}
        for line in lines:
            if line.startswith('event:'):
                current_event['event'] = line[6:].strip()
            elif line.startswith('data:'):
                data_content = line[5:].strip()
                try:
                    current_event['data'] = json.loads(data_content)
                except json.JSONDecodeError:
                    current_event['data'] = data_content
            elif line == '' and current_event:
                events.append(current_event)
                current_event = {}
        
        if current_event:
            events.append(current_event)
        
        return events
    
    async def test_connection(self) -> dict:
        """Testa la connessione base al MCP Server"""
        try:
            response = requests.get(self.mcp_url, timeout=10)
            return {
                "status": "success",
                "status_code": response.status_code,
                "note": "404 è normale per MCP server"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def initialize_mcp(self) -> dict:
        """Inizializza la connessione MCP"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "FastAPI-Client",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = requests.post(
                f"{self.mcp_url}/mcp",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                sse_events = self.parse_sse_response(response.text)
                
                # Cerca il risultato initialize
                initialize_result = None
                for event in sse_events:
                    if event.get('data', {}).get('id') == 1:
                        initialize_result = event.get('data', {})
                        break
                
                if initialize_result:
                    return {
                        "status": "success",
                        "protocol": "SSE",
                        "initialize_result": initialize_result,
                        "all_events": sse_events
                    }
                else:
                    return {
                        "status": "partial_success",
                        "protocol": "SSE",
                        "sse_events": sse_events,
                        "message": "Initialize result not found"
                    }
            else:
                return {
                    "status": "error",
                    "status_code": response.status_code,
                    "message": response.text
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def list_tools(self) -> dict:
        """Lista i tools disponibili sul server MCP"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            response = requests.post(
                f"{self.mcp_url}/mcp",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                sse_events = self.parse_sse_response(response.text)
                tools_data = None
                
                for event in sse_events:
                    if event.get('data', {}).get('id') == 2:
                        tools_data = event.get('data', {})
                        break
                
                return {
                    "status": "success",
                    "tools_data": tools_data,
                    "events": sse_events
                }
            else:
                return {
                    "status": "error",
                    "status_code": response.status_code,
                    "message": response.text
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def full_test(self) -> dict:
        """Test completo del server MCP"""
        test_results = {}
        
        # Test connessione
        test_results["connection"] = await self.test_connection()
        
        # Test initialize
        test_results["initialize"] = await self.initialize_mcp()
        
        # Test tools list (solo se initialize ha successo)
        if test_results["initialize"]["status"] == "success":
            test_results["tools_list"] = await self.list_tools()
        
        return test_results

# Client globale per l'app
mcp_client = MCPClient()

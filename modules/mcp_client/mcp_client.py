# python
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
        self.session_id = None  # ← AGGIUNGI QUESTA RIGA
    
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
    
    async def initialize_mcp(self) -> dict:
        """Inizializza la connessione MCP e memorizza session ID"""
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
                
                # Cerca il risultato initialize e session ID
                initialize_result = None
                for event in sse_events:
                    event_data = event.get('data', {})
                    if event_data.get('id') == 1:
                        initialize_result = event_data
                        # Estrai session ID dalla risposta
                        if 'result' in event_data:
                            self.session_id = event_data['result'].get('sessionId')
                        break
                
                if initialize_result:
                    return {
                        "status": "success",
                        "protocol": "SSE",
                        "initialize_result": initialize_result,
                        "session_id": self.session_id,
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
        """Lista i tools disponibili sul server MCP con session ID"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            # AGGIUNGI SESSION ID SE PRESENTE
            if self.session_id:
                payload["params"] = {"sessionId": self.session_id}
            
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

    # ... resto del codice invariato ...
    
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

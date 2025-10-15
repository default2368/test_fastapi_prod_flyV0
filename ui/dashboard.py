from nicegui import ui
from datetime import datetime
import requests
import json

class Dashboard:
    def __init__(self):
        self.fastapi_url = "https://test-mcp-prodv0.fly.dev"
        self.mcp_url = "https://test-mcp-prodv1.fly.dev"
        
    def create_header(self):
        """Crea l'header della dashboard"""
        with ui.header().classes('bg-blue-800 text-white p-4 shadow-lg'):
            with ui.row().classes('w-full justify-between items-center'):
                ui.label('🚀 MCP System Dashboard').classes('text-2xl font-bold')
                ui.label().bind_text_from(self, 'current_time').classes('text-lg')
                
    def create_sidebar(self):
        """Crea la sidebar con navigazione"""
        with ui.left_drawer().classes('bg-gray-100 p-4 w-64'):
            ui.label('🔧 Navigazione').classes('text-xl font-bold mb-4')
            
            with ui.column().classes('w-full gap-2'):
                ui.button('🏠 Dashboard', on_click=self.show_dashboard).classes('w-full')
                ui.button('🧪 Test Sistema', on_click=self.show_tests).classes('w-full')
                ui.button('🔗 Status MCP', on_click=self.show_mcp_status).classes('w-full')
                ui.button('📊 Metrics', on_click=self.show_metrics).classes('w-full')
                
    def create_main_content(self):
        """Crea l'area contenuto principale"""
        self.content = ui.column().classes('w-full p-8 gap-6')
        
    def show_dashboard(self):
        """Mostra la dashboard principale"""
        self.content.clear()
        
        with self.content:
            # Hero Section
            with ui.column().classes('w-full text-center mb-8'):
                ui.label('🎉 Benvenuto nel Sistema MCP').classes('text-4xl font-bold text-blue-800 mb-4')
                ui.label('Sistema integrato FastAPI + MCP Server deployato su Fly.io').classes('text-xl text-gray-600')
            
            # Cards Grid
            with ui.grid(columns=2).classes('w-full gap-6'):
                # Card FastAPI
                with ui.card().classes('p-6 shadow-lg border-l-4 border-green-500'):
                    with ui.column().classes('w-full gap-3'):
                        ui.label('🚀 FastAPI V0').classes('text-2xl font-bold text-green-700')
                        ui.label('Applicazione principale con endpoints REST').classes('text-gray-600')
                        ui.link('Visita API', f'{self.fastapi_url}/docs', new_tab=True).classes('text-blue-500 underline')
                        
                        with ui.row().classes('w-full justify-between mt-2'):
                            ui.button('Test', on_click=lambda: self.test_endpoint('/test')).classes('bg-green-500 text-white')
                            ui.button('Health', on_click=lambda: self.test_endpoint('/health')).classes('bg-blue-500 text-white')
                
                # Card MCP Server
                with ui.card().classes('p-6 shadow-lg border-l-4 border-purple-500'):
                    with ui.column().classes('w-full gap-3'):
                        ui.label('🤖 MCP Server V1').classes('text-2xl font-bold text-purple-700')
                        ui.label('Server Model Context Protocol per AI assistants').classes('text-gray-600')
                        ui.link('URL Server', self.mcp_url, new_tab=True).classes('text-blue-500 underline')
                        
                        with ui.row().classes('w-full justify-between mt-2'):
                            ui.button('Test MCP', on_click=lambda: self.test_endpoint('/test-mcp')).classes('bg-purple-500 text-white')
                            ui.button('Status', on_click=lambda: self.test_endpoint('/status')).classes('bg-blue-500 text-white')
            
            # Quick Actions
            with ui.card().classes('p-6 mt-6'):
                ui.label('⚡ Azioni Rapide').classes('text-xl font-bold mb-4')
                with ui.row().classes('w-full gap-4'):
                    ui.button('Test Completo V0', on_click=lambda: self.test_endpoint('/test-v0')).classes('bg-orange-500 text-white')
                    ui.button('Test Completo V1', on_click=lambda: self.test_endpoint('/test-v1')).classes('bg-indigo-500 text-white')
                    ui.button('Tutti i Test', on_click=self.run_all_tests).classes('bg-red-500 text-white')
    
    def show_tests(self):
        """Mostra la sezione test"""
        self.content.clear()
        
        with self.content:
            ui.label('🧪 Test del Sistema').classes('text-3xl font-bold mb-6')
            
            with ui.grid(columns=2).classes('w-full gap-6'):
                # Test V0
                with ui.card().classes('p-6'):
                    ui.label('🔧 Test V0 - FastAPI').classes('text-xl font-bold mb-4')
                    self.v0_result = ui.markdown('*Clicca per testare*').classes('min-h-20 p-4 bg-gray-50 rounded')
                    ui.button('Esegui Test V0', on_click=self.run_v0_test).classes('w-full bg-green-500 text-white')
                
                # Test V1
                with ui.card().classes('p-6'):
                    ui.label('🤖 Test V1 - MCP Server').classes('text-xl font-bold mb-4')
                    self.v1_result = ui.markdown('*Clicca per testare*').classes('min-h-20 p-4 bg-gray-50 rounded')
                    ui.button('Esegui Test V1', on_click=self.run_v1_test).classes('w-full bg-purple-500 text-white')
            
            # Test Rapidi
            with ui.card().classes('p-6 mt-6'):
                ui.label('🚀 Test Rapidi').classes('text-xl font-bold mb-4')
                with ui.row().classes('w-full gap-2'):
                    ui.button('Health Check', on_click=self.run_health_check).classes('bg-blue-500 text-white')
                    ui.button('Status Sistema', on_click=self.run_status_check).classes('bg-gray-500 text-white')
                    ui.button('Test MCP', on_click=self.run_mcp_test).classes('bg-indigo-500 text-white')
    
    def show_mcp_status(self):
        """Mostra lo status del MCP server"""
        self.content.clear()
        
        with self.content:
            ui.label('🔗 Status MCP Server').classes('text-3xl font-bold mb-6')
            
            with ui.card().classes('p-6 mb-6'):
                ui.label('📡 Informazioni Connessione').classes('text-xl font-bold mb-4')
                with ui.column().classes('gap-2'):
                    ui.label(f'**URL MCP Server:** {self.mcp_url}')
                    ui.label(f'**URL FastAPI:** {self.fastapi_url}')
            
            self.mcp_status_content = ui.column().classes('w-full gap-4')
            
            ui.button('🔄 Aggiorna Status', on_click=self.update_mcp_status).classes('bg-blue-500 text-white')
    
    def show_metrics(self):
        """Mostra metriche e statistiche"""
        self.content.clear()
        
        with self.content:
            ui.label('📊 Metriche di Sistema').classes('text-3xl font-bold mb-6')
            
            with ui.grid(columns=3).classes('w-full gap-4'):
                # Metric Card 1
                with ui.card().classes('p-4 text-center'):
                    ui.label('🟢').classes('text-3xl')
                    ui.label('FastAPI Status').classes('font-bold')
                    self.fastapi_status = ui.label('Checking...').classes('text-lg font-bold text-green-500')
                
                # Metric Card 2
                with ui.card().classes('p-4 text-center'):
                    ui.label('🟣').classes('text-3xl')
                    ui.label('MCP Status').classes('font-bold')
                    self.mcp_status = ui.label('Checking...').classes('text-lg font-bold text-purple-500')
                
                # Metric Card 3
                with ui.card().classes('p-4 text-center'):
                    ui.label('⏱️').classes('text-3xl')
                    ui.label('Ultimo Check').classes('font-bold')
                    self.last_check = ui.label(datetime.now().strftime('%H:%M:%S'))
            
            ui.button('🔄 Aggiorna Metriche', on_click=self.update_metrics).classes('bg-green-500 text-white')
    
    # Metodi di test
    async def test_endpoint(self, endpoint):
        """Testa un endpoint specifico"""
        try:
            response = requests.get(f"{self.fastapi_url}{endpoint}", timeout=10)
            result = json.dumps(response.json(), indent=2)
            ui.notify(f'✅ {endpoint} testato con successo!')
        except Exception as e:
            result = f"❌ Errore: {str(e)}"
            ui.notify(f'❌ Errore nel test {endpoint}')
        
        self.show_test_result(result)
    
    async def run_v0_test(self):
        """Esegue test V0"""
        self.v0_result.content = '🔄 Eseguendo test...'
        await self.test_endpoint('/test-v0')
        response = requests.get(f"{self.fastapi_url}/test-v0")
        result = json.dumps(response.json(), indent=2)
        self.v0_result.content = f'```json\n{result}\n```'
    
    async def run_v1_test(self):
        """Esegue test V1"""
        self.v1_result.content = '🔄 Eseguendo test...'
        await self.test_endpoint('/test-v1')
        response = requests.get(f"{self.fastapi_url}/test-v1")
        result = json.dumps(response.json(), indent=2)
        self.v1_result.content = f'```json\n{result}\n```'
    
    async def run_all_tests(self):
        """Esegue tutti i test"""
        await self.run_v0_test()
        await self.run_v1_test()
        ui.notify('🎉 Tutti i test completati!')
    
    async def run_health_check(self):
        await self.test_endpoint('/health')
    
    async def run_status_check(self):
        await self.test_endpoint('/status')
    
    async def run_mcp_test(self):
        await self.test_endpoint('/test-mcp')
    
    def show_test_result(self, result):
        """Mostra risultato test in un dialog"""
        with ui.dialog() as dialog, ui.card():
            ui.label('📋 Risultato Test').classes('text-xl font-bold mb-4')
            ui.code(result).classes('w-full max-h-96 overflow-auto')
            ui.button('Chiudi', on_click=dialog.close)
        dialog.open()
    
    async def update_mcp_status(self):
        """Aggiorna lo status MCP"""
        self.mcp_status_content.clear()
        with self.mcp_status_content:
            ui.linear_progress(0.5)  # Progress bar
            try:
                response = requests.get(f"{self.fastapi_url}/test-mcp", timeout=10)
                data = response.json()
                
                with ui.card().classes('p-4 bg-green-50 border-l-4 border-green-500'):
                    ui.label('✅ MCP Server Online').classes('text-lg font-bold text-green-700')
                    ui.label(f"Protocollo: {data.get('protocol', 'N/A')}").classes('text-sm')
                    ui.label(f"Server: {data.get('initialize_result', {}).get('result', {}).get('serverInfo', {}).get('name', 'N/A')}").classes('text-sm')
                    
            except Exception as e:
                with ui.card().classes('p-4 bg-red-50 border-l-4 border-red-500'):
                    ui.label('❌ MCP Server Offline').classes('text-lg font-bold text-red-700')
                    ui.label(f"Errore: {str(e)}").classes('text-sm')
    
    async def update_metrics(self):
        """Aggiorna le metriche"""
        try:
            # FastAPI status
            fastapi_response = requests.get(f"{self.fastapi_url}/health", timeout=5)
            fastapi_data = fastapi_response.json()
            self.fastapi_status.set_text(fastapi_data.get('fastapi_app', 'unknown').upper())
            
            # MCP status
            mcp_response = requests.get(f"{self.fastapi_url}/test-mcp", timeout=5)
            mcp_data = mcp_response.json()
            self.mcp_status.set_text(mcp_data.get('mcp_server_status', 'unknown').upper())
            
            # Last check
            self.last_check.set_text(datetime.now().strftime('%H:%M:%S'))
            
            ui.notify('✅ Metriche aggiornate!')
        except Exception as e:
            ui.notify(f'❌ Errore aggiornamento metriche: {e}')
    
    @property
    def current_time(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def create_ui(self):
        """Crea l'interfaccia completa"""
        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        self.show_dashboard()
        
        # Aggiorna metriche all'avvio
        ui.timer(30.0, self.update_metrics)  # Aggiorna ogni 30 secondi

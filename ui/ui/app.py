from nicegui import app, ui
from .dashboard import Dashboard

def create_ui():
    """Crea l'interfaccia NiceGUI principale"""
    
    # Configurazione della pagina
    ui.page_title('MCP System Dashboard')
    
    # Crea il dashboard
    dashboard = Dashboard()
    dashboard.create_ui()
    
    # Footer
    with ui.footer().classes('bg-gray-800 text-white p-4 text-center'):
        ui.label('🚀 MCP System - Deployato su Fly.io').classes('text-sm')
        ui.label('FastAPI V0 + MCP Server V1').classes('text-xs text-gray-400')

# Avvia l'app quando il modulo è eseguito direttamente
if __name__ in {'__main__', '__mp_main__'}:
    create_ui()
    ui.run(title="MCP Dashboard", host='0.0.0.0', port=8080)

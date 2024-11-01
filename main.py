from app_flow_manager import AppManager
from render_manager import RenderManager
from config_settings import db_config


if __name__ == "__main__":
    # Create and run the app
    render_manager = RenderManager("./styles/styles.css", "./templates")
    app = AppManager(db_config, render_manager)
    app.main_panel_content()

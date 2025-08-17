'''
Made by: Eduardo Reyes, Ph.D.
Contact: ed5reyes@outlook

Version: 1.0
Date: Aug 16, 2025
Notes: User similar but simplified approach for this hub as done for BBI_projects.
'''

import streamlit as st
import subprocess
import os
import socket
import shlex
import configparser
from typing import Optional, List, Dict, Any

# --- Configuration ---
# The hub is in 'Streamlit_projects/000_App_hub/'. The project root is one level up.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "app_status.txt")

st.set_page_config(page_title="Streamlit Project Hub", layout="wide")
st.title("🚀 Streamlit Project Hub")

# --- Core Logic ---
@st.cache_data
def load_app_config(config_path: str) -> Dict[str, Dict[str, Any]]:
    """Loads app metadata from the configuration file."""
    config = configparser.ConfigParser()
    if not os.path.exists(config_path):
        return {}

    with open(config_path, "r", encoding="utf-8") as f:
        config.read_file(f)

    apps = {}
    for section in config.sections():
        # Assuming all sections in the config are Streamlit apps
        apps[section] = {
            "path": config[section].get("path", ""),
            "entry": config[section].get("entry", "app.py"),
            "icon": config[section].get("icon", "🎈"),
            "status": config[section].get("status", "").lower(),
            "message": config[section].get("message", ""),
            "args": shlex.split(config[section].get("args", "")),
        }
    return apps

def find_free_port(start: int = 8502, end: int = 8600) -> Optional[int]:
    """Finds an available TCP port in a given range."""
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("localhost", port)) != 0:
                return port
    return None

def launch_streamlit_app(app_dir: str, entry_script: str, port: int, args: List[str]):
    """Launches a Streamlit app in a separate process."""
    abs_path = os.path.join(BASE_DIR, app_dir)
    command = [
        "streamlit", "run", entry_script,
        "--server.port", str(port),
        "--server.headless", "true",
    ]
    if args:
        command.append("--")
        command.extend(args)

    # Using DEVNULL to prevent console windows from popping up on Windows
    subprocess.Popen(
        command,
        cwd=abs_path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

# --- Session State Management ---
if "launched_apps" not in st.session_state:
    # Simplified session state: {app_name: port}
    st.session_state.launched_apps = {}

# --- UI Rendering ---
def render_app_row(name: str, config: Dict[str, Any]):
    """Renders a single row for an app in the hub."""
    port = st.session_state.launched_apps.get(name)
    is_launched = port is not None

    col1, col2, col3 = st.columns([5, 1, 4], gap="medium")

    with col1:
        st.markdown(f"### {config['icon']} {name}")

    with col2:
        if not is_launched:
            if st.button("Launch", key=f"launch_{name}", type="primary", use_container_width=True):
                new_port = find_free_port()
                if new_port is None:
                    st.error("⚠️ No available ports to launch the app!")
                    return

                launch_streamlit_app(config["path"], config["entry"], new_port, config["args"])
                st.session_state.launched_apps[name] = new_port
                st.rerun()
        else:
            open_link = f"http://localhost:{port}"
            open_button_html = f"""
                    <a href="{open_link}" target="_blank">
                        <button style="
                            background-color: #28a745;
                            color: white;
                            border: none;
                            padding: 0.4em 1.2em;
                            border-radius: 5px;
                            font-weight: bold;
                            cursor: pointer;
                        ">Open</button>
                    </a>
                """
            st.markdown(open_button_html, unsafe_allow_html=True)

    with col3:
        status = config.get("status")
        message = config.get("message")
        if status and message:
            # Dynamically call the correct status message type (e.g., st.success, st.warning)
            if hasattr(st, status):
                getattr(st, status)(message)
            else:
                st.info(message) # Default to info

# --- Main App ---
all_apps = load_app_config(CONFIG_FILE)

if not all_apps:
    st.warning(f"No applications are configured. Please create or check `{CONFIG_FILE}`.")
else:
    with st.container(border=True):
        for app_name, app_config in all_apps.items():
            render_app_row(app_name, app_config)
import streamlit as st
import os
from app.executor import execute_in_wsl
from app.nlp_parser import get_bash_command
from app.safety_checker import is_safe_command
from app.agents.installer_agent import InstallerAgent
from app.agents.downloader_agent import DownloaderAgent
from app.file_manager import list_files, delete_file

st.set_page_config(page_title="SmartShell AI", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🤖 Welcome to SmartShell AI</h1>
    <h4 style='text-align: center; color: gray;'>Transforming natural language into powerful Bash commands</h4>
""", unsafe_allow_html=True)

st.divider()



# Center the image using layout utilities
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("assets/robot.png", width=200)



# Dark mode toggle
dark_mode = st.checkbox("🌙 Dark Mode")

# Create a user_uploads directory if it doesn't exist
upload_folder = "user_uploads"
os.makedirs(upload_folder, exist_ok=True)

# Additional functionalities
st.sidebar.subheader("📂 Manage Files")
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["txt", "csv", "json", "py"])

if uploaded_file is not None:
    with open(os.path.join(upload_folder, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"{uploaded_file.name} uploaded to {upload_folder}.")

if st.sidebar.button("Clear All Files"):
    for file in os.listdir(upload_folder):
        os.remove(os.path.join(upload_folder, file))
    st.sidebar.success("All files cleared.")

# Command Execution Log
st.subheader("📜 Command Log")
if "command_log" not in st.session_state:
    st.session_state.command_log = []

option = st.radio(
    "What would you like to do?",
    (
        "Manual input (Linux command or install package)",
        "Voice input (download URL) [WSL unsupported]",
        "Resume a download",
        "Exit"
    )
)

if option == "Manual input (Linux command or install package)":
    user_input = st.text_input("Enter your Linux task:")
    if st.button("Execute"):
        if not user_input.strip():
            st.warning("Please enter a command.")
        else:
            if "install" in user_input.lower():
                installer = InstallerAgent()
                installer.install_package(user_input.split()[-1])
            else:
                bash_command = get_bash_command(user_input)
                st.markdown(f"*Interpreted Bash Command:* {bash_command}")
                if is_safe_command(bash_command):
                    output = execute_in_wsl(bash_command)
                    st.session_state.command_log.append(f"{user_input} -> {output}")
                    st.code(output or "✅ Command executed successfully.")
                else:
                    st.error("🚨 Unsafe command detected! Not executing.")

elif option == "Voice input (download URL) [WSL unsupported]":
    st.warning("🎤 Voice input is not supported in WSL. Use manual mode instead.")

elif option == "Resume a download":
    url = st.text_input("Enter the file URL to resume download:")
    if st.button("Resume Download"):
        if url:
            downloader = DownloaderAgent(download_dir=upload_folder)
            status = downloader.download_with_resume(url)
            st.success(status)
        else:
            st.warning("Please enter a valid URL.")

elif option == "Exit":
    st.info("👋 Exiting session. Close the tab to leave.")

st.divider()

st.subheader("📁 File Library")
files = list_files(upload_folder)

if files:
    for f in files:
        with st.expander(f):
            file_path = os.path.join(upload_folder, f)

            # Display file content for text and Python files
            if f.endswith(".txt") or f.endswith(".py"):
                try:
                    with open(file_path, "r") as file:
                        st.code(file.read())
                except Exception as e:
                    st.warning(f"Error reading {f}: {e}")

            # Download button with error handling
            try:
                with open(file_path, "rb") as file:
                    st.download_button("Download", file, file_name=f)
            except FileNotFoundError:
                st.warning(f"File {f} not found for download.")

            # Delete button with proper state handling
            if st.button(f"Delete {f}", key=f"delete_{f}"):
                if delete_file(upload_folder, f):
                    st.success(f"{f} deleted.")
                    st.experimental_rerun()
                else:
                    st.warning(f"Failed to delete {f}.")
else:
    st.text("No files available yet.")



#%% libs

import warnings
# ignore only warnings whose message contains "st.experimental_user"
warnings.filterwarnings("ignore", message=".*st.experimental_user.*")

import os
import io
import time
import zipfile
import shutil
import streamlit as st
import tempfile
import sys
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime import Runtime

from utils import prune_old_temp_dirs, safe_extract_zip_bytes

#%% init uploader

PATH = os.path.dirname(__file__)
TEMP_BASE = os.path.join(tempfile.gettempdir(), "mlviewer_uploads")  

# PATH = os.getcwd()
sys.path.append(PATH)
os.makedirs(TEMP_BASE, exist_ok=True)


def handle_upload_ui():
    # Prune old session dirs each time the home page loads
    prune_old_temp_dirs(TEMP_BASE)

    st.header("Upload dataset (data.zip)")
    st.write("Upload a file to start exploring the data. Use 'Finish session button' to remove the zip and/or finish the session.")

    uploaded = st.file_uploader("Upload data.zip", type=["zip"])
    if uploaded is not None:
        if st.button("Extract and use this ZIP"):
            # create a unique session temp dir
            upload_dir = tempfile.mkdtemp(prefix="mlviewer_", dir=TEMP_BASE)
            try:
                zip_bytes = io.BytesIO(uploaded.read())
                safe_extract_zip_bytes(zip_bytes, upload_dir)
            except Exception as e:
                # cleanup on failure
                try:
                    shutil.rmtree(upload_dir)
                except Exception:
                    pass
                st.error(f"Failed to extract zip: {e}")
                return

            # save into session_state for use across pages in this session
            st.session_state["data_root"] = upload_dir
            st.success(f"Uploaded and extracted to session folder.")


    # If already uploaded in this session, show controls
    data_root = st.session_state.get("data_root")
    if data_root and os.path.isdir(data_root):
        st.info("You have an active upload for this session.")
        # st.write(data_root)
        if st.sidebar.button("Finish session and remove my upload"):
            try:
                shutil.rmtree(data_root)
            except Exception as e:
                st.warning(f"Could not delete upload directory: {e}")
            st.session_state.pop("data_root", None)
            st.success("Your upload was removed.")
            st.stop()



#%% app

if __name__ == "__main__":

    st.set_page_config(layout="wide")
    st.title("**HOME**")
    st.divider()
    st.write('Select a project from the sidebar to start exploring the data')

    def count_sessions_unsafe():
        # Find the global Runtime object
        import gc
        rt = next(o for o in gc.get_objects() if isinstance(o, Runtime))
        # Session manager may be accessible like this in some versions:
        sess_mgr = rt._session_mgr  # private
        # Each session has websocket(s); count those considered active
        return len(list(sess_mgr.list_sessions()))  

    st.write("Connected sessions:", count_sessions_unsafe())
    st.divider()
    st.write("To have access to the data, you should contact the administrator.\n Data are provided in a zip folder and must be uploaded by the user.")
    # add link
    link = 'https://cimafoundation.sharepoint.com/:f:/s/AmbitoIncendi/EnZ_tObryKxCteu4VKFAJVkB7DEDPKWwkTdAGOGIUsb8Yg?e=Z6kABK'
    st.markdown(f"👉 link to private [data]({link})", unsafe_allow_html=True)
    st.write("**Note:** Uploaded data is temporary and will be deleted when the session ends or after a period of inactivity.")
    st.divider()

    handle_upload_ui()


    
#%%
# import yaml
# import streamlit_authenticator as stauth
# from auth import login_widget, logout_widget

# try:
#     auth_status = login_widget()  # visible login on main page
# except Exception as e:  # None (widget shown, not yet submitted)
#     # st.error("Username/password incorrect")
#     st.error(str(e))
#     # st.stop()
# #a dd it in sessions tate car
# if "login" not in st.session_state:
#     st.session_state["login"] = auth_status

# if 'logout' not in st.session_state:
#     st.session_state['logout'] = False

# if st.session_state.get('authentication_status'):
#     logout_widget(key = 'logut_home')
#     handle_upload_ui()
# elif st.session_state.get('authentication_status') is False:
#     st.error('Username/password is incorrect')
# elif st.session_state.get('authentication_status') is None:
#     st.warning('Please enter your username and password')


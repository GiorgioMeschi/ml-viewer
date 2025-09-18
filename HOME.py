

#%%

import os
import sys
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime import Runtime


PATH = os.path.dirname(__file__)
# PATH = os.getcwd()
sys.path.append(PATH)

#%% global vars

DATAPATH = '/home/fremen/workspaces/GM/projects/viewer/ml-viewer/data'


#%% app

st.set_page_config(layout="wide")

if __name__ == '__main__':
    st.write('Select a project from the sidebar to start exploring the data')

    def count_sessions_unsafe():
        # Find the global Runtime object
        import gc
        rt = next(o for o in gc.get_objects() if isinstance(o, Runtime))
        # Session manager may be accessible like this in some versions:
        sess_mgr = rt._session_mgr  # private
        # Each session has websocket(s); count those considered active
        return len(list(sess_mgr.list_sessions()))  # method name varies by version!

    st.write("Connected sessions:", count_sessions_unsafe())

#%%




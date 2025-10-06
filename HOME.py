

#%%

import os
import sys
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime import Runtime


import yaml
import streamlit as st
import streamlit_authenticator as stauth


from auth import login_widget, logout_widget

try:
    auth_status = login_widget()  # visible login on main page
except Exception as e:  # None (widget shown, not yet submitted)
    # st.error("Username/password incorrect")
    st.error(str(e))
    # st.stop()

# #a dd it in sessions tate car
# if "login" not in st.session_state:
#     st.session_state["login"] = auth_status

# if 'logout' not in st.session_state:
#     st.session_state['logout'] = False

if st.session_state.get('authentication_status'):
    logout_widget(key = 'logut_home')
    st.write(f'Welcome *{st.session_state.get("name")}*')

    PATH = os.path.dirname(__file__)
    # PATH = os.getcwd()
    sys.path.append(PATH)

    # global vars
    DATAPATH = f'{PATH}/data'

    # app
    st.set_page_config(layout="wide")

    # if __name__ == '__main__':
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

elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')



# st.sidebar.success(f"Logged in as {name} ({username})")
# if st.sidebar.button("Log out"):
#     logout_widget()
#     st.session_state["logout"] = True
#     auth_status = False
#     st.session_state["login"] = False
#     # st.stop()
#     # rerun
#     st.rerun()
#     # st.experimental_rerun()



    
#%%




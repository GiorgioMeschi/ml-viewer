import streamlit as st
from PIL import Image
import os
import shutil
import time
import zipfile
import pandas as pd

p = os.path.dirname(os.path.dirname(__file__) )
sys.path.append(p)

from stats import show_table, plot_historical_stats

TTL_SECONDS = 60 * 60 * 6         # auto-delete uploads older than 6 hours when session restart


def plot_img(path, w = None):
    try:    
        img = Image.open(path)
        if w is None:
            st.image(img)
        else:
            st.image(img, width = w)
    except:
        st.write('No image available')



def prune_old_temp_dirs(temp_base):
    """Remove temp upload dirs older than TTL_SECONDS (best-effort)."""
    now = time.time()
    try:
        for name in os.listdir(temp_base):
            path = os.path.join(temp_base, name)
            if not os.path.isdir(path):
                continue
            mtime = os.path.getmtime(path)
            if now - mtime > TTL_SECONDS:
                try:
                    shutil.rmtree(path)
                except Exception:
                    pass
    except FileNotFoundError:
        pass

def safe_extract_zip_bytes(zip_bytes_io, target_dir):
    '''
    extract zip folder provided by the user.
    '''
    total = 0
    count = 0
    with zipfile.ZipFile(zip_bytes_io) as zf:
        for member in zf.infolist():
            if member.is_dir():
                continue
            member_name = member.filename
            # Prevent path traversal attacks
            if os.path.isabs(member_name) or ".." in os.path.normpath(member_name).split(os.path.sep):
                raise RuntimeError(f"Unsafe filename in zip: {member_name}")
            total += member.file_size
            count += 1
            dest_path = os.path.join(target_dir, member_name)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with zf.open(member, "r") as source, open(dest_path, "wb") as target:
                shutil.copyfileobj(source, target)
    return True


def access_data():
    '''
    acces data folder across pages
    '''

    data_root = st.session_state.get("data_root")
    if not data_root or not os.path.isdir(data_root):
        st.info("No uploaded dataset for this session. Please upload on the Home page.")
        st.stop()
    
    if st.sidebar.button("Finish session and remove my upload"):
        try:
            shutil.rmtree(data_root)
        except Exception as e:
            st.warning(f"Could not delete upload directory: {e}")
        st.session_state.pop("data_root", None)
        st.success("Your upload was removed.")
        st.stop()

    return data_root


def show_burned_pixel_per_susc_class(project_datapath):

    with st.expander("View Historical Stats"):

        # create 3 columsn the ceter 75% wide
        endcols = st.columns([1,6,1])
        with endcols[1]:

            # radio button with showing the table in percentage or not
            st.subheader('Number of burned pixels per susceptibility class')
            show_perc = st.radio("Show values as percentage?", ('No', 'Yes'), index=0, horizontal=True)
            if show_perc == 'Yes':
                with st.expander("Show Table"):
                    table_file = f'{project_datapath}/statistics/table_ba_susc_perc.csv'
                    rounds = 2
                    available = show_table(table_file, rounds)
                if available:
                    with st.expander("Plot Historical Stats"):
                        plot_historical_stats(pd.read_csv(table_file, index_col=0))

            else:
                with st.expander("Show Table"):
                    table_file = f'{project_datapath}/statistics/table_ba_susc.csv'
                    rounds = 0
                    available = show_table(table_file, rounds)
                if available:
                    with st.expander("Plot Historical Stats"):
                        plot_historical_stats(pd.read_csv(table_file, index_col=0))

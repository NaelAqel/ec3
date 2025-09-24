import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")

st.title("EC3 Tester")

st.markdown("""#### Instructions
- Write your query below then click on **`Run Query`** button  
- You will see the first 20 rows maximum of the query output
- If you got an error, fix the query and **click on `Run Query` again**
""")

run = st.button("Run Query")

# --- Layout: Two columns ---
col1, col2 = st.columns([1, 1])  # col1 for input, col2 for results


# --- Database setup ---
DB_FILE = "AdventureWorks.db"

# Initialize session state for query
if "query" not in st.session_state:
    st.session_state.query = ""  # initial empty query

with col1:
    query = st.text_area(
            label="Write your SQL query here:",
            value=st.session_state.query,
            height=1000
        )
    
    st.session_state.query = query  # save latest query

with col2:
    st.markdown("#### Results (Max 20 Rows)")
    output_placeholder = st.empty()  # Placeholder to write results or errors

    # --- Run Query ---
    if run:
        if not query.strip():
            output_placeholder.warning("Please write a SQL query first!")
        else:
            try:
                with sqlite3.connect(DB_FILE) as conn:
                    df = pd.read_sql_query(query, conn)
                
                if df.empty:
                    output_placeholder.info("Query ran successfully but returned no results.")
                else:
                    output_placeholder.dataframe(df.head(20), width='stretch')
            except Exception as e:
                # Extract only the message without the query
                msg = str(e)
                # Some SQLite errors start with "Execution failed on sql '...': ...", strip that part
                if "Execution failed on sql" in msg:
                    msg = msg.split(":", 1)[-1].strip()
                output_placeholder.error(f"**Error {msg}**\n\n\nFix the query and click on `Run Query` again")
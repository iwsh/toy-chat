import streamlit as st
import time
import os
import datetime
import pandas as pd

data_dir = "data/"

def main():
    st.title("Hello Chat")

    user = st.text_input("Username")
    msg_body = st.text_area("Message")
    if st.button('Send'):
        send_message(user, msg_body)

    for _, msg in get_messages():
        st.write(f"**{msg.user}**")
        st.write(f"{msg.body}")


def send_message(user, msg_body):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    df = pd.DataFrame([[user, msg_body, now]])
    df = df.rename(columns={0:"user",1:"body",2:"datetime"})
    df.to_parquet(path=data_dir, partition_cols="datetime")


def get_messages():
    try:
        df_msgs = pd.read_parquet(path=data_dir)
        return df_msgs.iterrows()
    except FileNotFoundError:
        st.write("No Messages")
        return []


if __name__ == "__main__":
    main()
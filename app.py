import streamlit as st
import json
from confluent_kafka import Consumer
from config import bootstrap_servers, topic

st.set_page_config(page_title='Data Stock Data', layout='wide')


if 'log_loss' not in st.session_state:
    st.session_state['log_loss'] = []


conf = {'bootstrap.servers': bootstrap_servers, 'group.id': 'my_consumers'}

consumer = Consumer(conf)

consumer.subscribe([topic])

st.title('Training logloss')

chart_holder = st.empty()

while True:
    message = consumer.poll(1000)
    if message is None:
        st.write("Нет новых сообщений...")
    if message is not None:
        stock_data = json.loads(message.value().decode('utf-8'))

    st.session_state['log_loss'].append(stock_data['log_loss'])
    chart_holder.line_chart(st.session_state['log_loss'])



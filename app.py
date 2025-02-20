import streamlit as st
import json
from confluent_kafka import Consumer
from config import bootstrap_servers_kafka0, topic_train_metrics

st.set_page_config(page_title='Training Metrics', layout='wide')

conf = {'bootstrap.servers': bootstrap_servers_kafka0, 'group.id': 'my_consumers'}
consumer = Consumer(conf)
consumer.subscribe([topic_train_metrics])

st.title('Training Metrics')

# Храним несколько метрик в session_state
metrics = ['log_loss', 'rmse', 'mae', 'error', 'auc']
chart_containers = {}
# Инициализируем метрики, если они не существуют в session_state
for metric in metrics:
    if metric not in st.session_state:
        if metric not in chart_containers:
            chart_containers[metric] = None
        st.session_state[metric] = []
        st.subheader(f'{metric}')
        chart_containers[metric] = st.empty()

# Отображаем каждый график для метрики
while True:
    message = consumer.poll(1000)
    
    if message is None:
        st.write("Нет новых сообщений...")
        continue
    
    stock_data = json.loads(message.value().decode('utf-8'))

    # Добавляем данные в session_state для каждой метрики
    for key, value in stock_data.items():
        if key in metrics:
            st.session_state[key].append(value)
    
    # Отображаем графики для каждой метрики
    for metric in metrics:
        if len(st.session_state[metric]) > 0:
            chart_containers[metric].line_chart(st.session_state[metric])

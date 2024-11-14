import random
import pandas as pd

# Заданные параметры
dTz = 0.724  # Время между заявками
mu1 = 1.412  # Параметр экспоненциального распределения для обслуживания
num_events = 100  # Число событий для моделирования

# Инициализация переменных
current_time = 0.0
state = 0  # Начальное состояние СМО
next_arrival_time = dTz
next_service_time = -1
event_data = []
request_data = []
state_counts = {0: 0, 1: 0}
total_time_in_state = {0: 0.0, 1: 0.0}

# Переменные для анализа
#request_id = 0
#served_requests = 0
#rejected_requests = 0
busy_time = 0.0

# Основной цикл моделирования
#for event_num in range(1, num_events + 1):
#    # Определение типа события и его времени
#    if state == 0:
#        event_type = 1  # Поступление заявки
#        current_time = next_arrival_time
#        service_time = random.expovariate(mu1)
#        next_service_time = current_time + service_time
#    else:
#        if next_arrival_time < next_service_time:
#            event_type = 3  # Отказ в обслуживании
#            current_time = next_arrival_time
#            service_time = 0
#            next_service_time = current_time
#        else:
#            event_type = 2  # Завершение обслуживания
#            current_time = next_service_time
# Инициализация переменных
request_id = 0  # Номер текущей заявки
served_requests = 0  # Обслуженные заявки
rejected_requests = 0  # Отклоненные заявки

# Основной цикл моделирования
for event_num in range(1, num_events + 1):
    if state == 0:  # Система в состоянии 0
        event_type = 1  # Поступление новой заявки
        current_time = next_arrival_time
        service_time = random.expovariate(mu1)
        next_service_time = current_time + service_time
        request_id += 1  # Увеличиваем номер заявки только здесь
        state = 1  # Система переходит в состояние 1
        event_data.append([event_num, current_time, event_type, state, service_time, next_arrival_time, request_id])
        next_arrival_time = current_time + dTz  # Обновляем время следующего прихода

    else:  # Система в состоянии 1
        if next_arrival_time < next_service_time:
            event_type = 3  # Отказ в обслуживании
            current_time = next_arrival_time
            rejected_requests += 1
            event_data.append([event_num, current_time, event_type, state, 0, next_arrival_time, request_id + 1])  # Номер отказанной заявки
            next_arrival_time = current_time + dTz  # Обновляем время следующего прихода
        else:
            event_type = 2  # Завершение обслуживания
            current_time = next_service_time
            served_requests += 1
            state = 0  # Система переходит в состояние 0
            event_data.append([event_num, current_time, event_type, state, -1, next_arrival_time, request_id])


    # Обновление состояния системы и сбор данных
    if event_type == 1:  # Поступление заявки и начало обслуживания
        state = 1
        request_id += 1
        busy_time += service_time
        request_data.append([request_id, current_time, service_time, current_time + service_time])
        next_arrival_time = current_time + dTz
        state_counts[0] += 1
        event_data.append([event_num, current_time, event_type, state, service_time, dTz, request_id])
    
    elif event_type == 2:  # Завершение обслуживания
        state = 0
        next_service_time = -1
        state_counts[1] += 1
        served_requests += 1
        event_data.append([event_num, current_time, event_type, state, -1, dTz, request_id])
    
    elif event_type == 3:  # Отказ в обслуживании
        state = 1
        rejected_requests += 1
        next_arrival_time = current_time + dTz
        state_counts[1] += 1
        event_data.append([event_num, current_time, event_type, state, next_service_time - current_time, dTz, request_id + 1])
        request_data.append([request_id + 1, current_time, 0, current_time])

    # Обновление времени пребывания в каждом состоянии
    total_time_in_state[state] += dTz if event_type == 1 else current_time

# Создание таблиц и расчет итоговых значений
events_df = pd.DataFrame(event_data, columns=["Event #", "Event Time", "Type", "State", "Remaining Service Time", "Next Arrival Time", "Request #"])
requests_df = pd.DataFrame(request_data, columns=["Request #", "Arrival Time", "Service Time", "Completion Time"])

# Итоговая таблица состояний
total_time = sum(total_time_in_state.values())
state_stats = {
    "State": [0, 1],
    "R_i(100)": [state_counts[0], state_counts[1]],
    "v_i(100)": [state_counts[0] / num_events, state_counts[1] / num_events],
    "T_i(100)": [total_time_in_state[0], total_time_in_state[1]],
    "delta_i(100)": [total_time_in_state[0] / total_time, total_time_in_state[1] / total_time]
}
states_df = pd.DataFrame(state_stats)

# Вычисляем итоговые значения
total_requests = request_id
total_served = served_requests
total_rejected = rejected_requests
idle_time = total_time - busy_time

pd.options.display.max_rows = None

# Вывод результатов
print("Таблица событий:")
print(events_df)  # Вывод первых 10 строк для проверки

print("\nТаблица заявок:")
print(requests_df)  # Вывод первых 10 строк для проверки

print("\nТаблица состояний:")
print(states_df)

print("\nИтоговые значения:")
print(f"Число заявок, поступивших в СМО: {total_requests}")
print(f"Число полностью обслуженных заявок: {total_served}")
print(f"Число отклоненных заявок: {total_rejected}")
print(f"Общее время занятости прибора: {busy_time}")
print(f"Общее время простоя прибора: {idle_time}")


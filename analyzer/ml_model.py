import numpy as np
import pandas as pd
import torch
from torch import nn


# Data Generattion
def generate_message_activity(hw, target=1, max_interval=10):
    noise_strength = np.random.randint(4, size=1)
    x = np.array(list(range(0, hw)))
    y = np.sin(x)  + 1 + np.random.randint(4, size=len(x))#*noise_strength
    step = np.random.choice([0, 0.1, 0.15, 0.25, 0.3, 0.4, 0.5])
    sv = int(step * hw)
    y[sv:] += x[sv:]/2 + abs(y[sv])
    y *= max_interval / 10
    if target == 0:
        return y[::-1] / 4
    return y / 4


def generate_message_activity_plane(hw, target=1, max_interval=10):
    noise_strength = 0.5
    x = np.array(list(range(0, hw)))
    h = 1 + np.random.randint(2, size=1) if target == 0 else 5+np.random.randint(4, size=1)
    t = 1 if target == 0 else 1+np.random.randint(2, size=1)
    y = t * np.sin(x) + h + np.random.randint(3, size=len(x))*noise_strength
    y *= max_interval / 10
    return y


def generate_by(hw, plane, pos, max_interval):
    if plane:
        return generate_message_activity_plane(hw, pos, max_interval)
    else:
        return generate_message_activity(hw, pos, max_interval)


def gen_historic_data(hw = 40, c = 7, pos_size = 0.8, last_pos= 0, max_interval=13):
    hist = []
    last = None
    target = None
    
    for _ in range(int(c * pos_size)):
        hist.append(generate_by(hw, np.random.choice([0, 1]), 1, max_interval))
    for _ in range(int(c * (1 - pos_size))):
        hist.append(generate_by(hw, np.random.choice([0, 1]), 0, max_interval))
    hist = np.array(hist).mean(axis=0)
    
    if pos_size > 0.5:
        if last_pos:
            last = generate_by(hw, np.random.choice([0, 1]), 1, max_interval)
            target = 1
        else:
            last = generate_by(hw, np.random.choice([0, 1]), 0, max_interval)
            target = 0
    else:
        plane = np.random.choice([0, 1])
        if last_pos:
            last = generate_by(hw, plane, 1, max_interval)
            target = 1
        else:
            last = generate_by(hw, plane, 0, max_interval)
            if not plane:
                target = 1
            else:
                target = 0
    activity_series = np.concatenate((hist, last))
    
    return activity_series, target


def gen_dataset(hw, c, size):
    activity = []
    target = []
    
    for _ in range(size):
        pos_size = np.random.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        last_pos = np.random.choice([0, 1])
        act, targ = gen_historic_data(hw=hw, c=c, pos_size=pos_size, last_pos=last_pos)
        activity.append(act)
        target.append(targ)
        

def gen_worker_df(hw, c, max_range):
    df_dict = {}
    for k in max_range:
        pos_size = np.random.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        last_pos = np.random.choice([0, 1])
        df_dict[k] = gen_historic_data(hw=hw, c=c, pos_size=pos_size, last_pos=last_pos, max_interval=max_range[k])[0].astype(int)
    return df_dict


# Model utils
class LSTMClassifier(nn.Module):
    """Very simple implementation of LSTM-based time-series classifier."""
    
    def __init__(self, input_dim, hidden_dim, layer_dim, output_dim):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.layer_dim = layer_dim
        self.rnn_1 = nn.LSTM(input_dim, hidden_dim, layer_dim, batch_first=True)
        self.rnn_2 = nn.LSTM(input_dim, hidden_dim, layer_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim*2, output_dim)
        self.batch_size = None
        self.hidden = None
    
    def forward(self, x1, x2):
        h0, c0 = self.init_hidden(x1)
        out1, (hn, cn) = self.rnn_1(x1, (h0, c0))
        h0, c0 = self.init_hidden(x2)
        out2, (hn, cn) = self.rnn_2(x2, (h0, c0))
        out = torch.cat([out1[:, -1, :], out2[:, -1, :]], axis=1)
        out = torch.sigmoid(self.fc(out))
        return out
    
    def init_hidden(self, x):
        h0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim)
        c0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim)
        return [t.cpu() for t in (h0, c0)]

    
def scale(sample_mat, interval_max):
    scaled_mat = sample_mat / interval_max
    return scaled_mat
    
    
def scale_by_max(worker, max_range):
    wk_dict = worker.to_dict(orient="list")
    scaled_worker = {}
    for k in max_range:
        scaled_worker[k] = scale(np.array(wk_dict[k]), max_range[k])
    return scaled_worker
    

def predict_by_max(model, scaled_worker_interval_1, scaled_worker_interval_2, type_up):
    proba = 0
    for k in type_up:
        x1 = torch.tensor(scaled_worker_interval_1[k]).unsqueeze(0).unsqueeze(2).float()
        x2 = torch.tensor(scaled_worker_interval_2[k]).unsqueeze(0).unsqueeze(2).float()
        pred = model(x1, x2).item()
        if not type_up[k]:
            pred = 1 - pred
        proba += pred
    return 1 - proba  / len(type_up)    

def to_worker_format(form):
    res = {}
    for k in form[0].dict():
        res[k] = []
    for row in form:
        row_d = row.dict()
        for k in row_d:
            res[k].append(row_d[k])
    return pd.DataFrame(res)

    
def predict(worker_interval_1, worker_interval_2):
    model_path = "lstm_siam_v2.pth"
    
    input_dim = 1    
    hidden_dim = 256
    layer_dim = 3
    output_dim = 1
    
    print("Инициализируем модель...")
    model = LSTMClassifier(input_dim, hidden_dim, layer_dim, output_dim)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    
    # Максимум в диапазоне для каждой статистики 
    max_range = {"sent_messages_count": 10,
                "received_messages_count": 10, 
                "recipient_counts": 10, 
                "bcc_count": 10, 
                "cc_count": 10, 
                "read_messages_later_than": 10, 
                "days_between_received_and_read": 14,
                "replied_messages_count": 10, 
                "sent_characters_count": 5400, 
                "messages_outside_working_hours": 10, 
                "messages_with_question_and_no_reply": 5}
    
    # 0 - увеличение статистики ведет к увольнению, 1 - наоборот 
    type_up = {"sent_messages_count": 1,
                "received_messages_count": 1, 
                "recipient_counts": 1, 
                "bcc_count": 1, 
                "cc_count": 1, 
                "read_messages_later_than": 0, 
                "days_between_received_and_read": 0,
                "replied_messages_count": 1,
                "sent_characters_count": 1, 
                "messages_outside_working_hours": 0, 
                #"received_to_sent_ratio": 1, 
                "messages_with_question_and_no_reply": 0}
    
    
    # Делаем предскзазание
    scaled_worker_interval_1 = scale_by_max(to_worker_format(worker_interval_1), max_range)
    scaled_worker_interval_2 = scale_by_max(to_worker_format(worker_interval_2), max_range)
    
    return predict_by_max(model, scaled_worker_interval_1, scaled_worker_interval_2, type_up)
    
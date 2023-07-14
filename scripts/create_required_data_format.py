import json
from datasets import load_dataset
from huggingface_hub import login

file_path = "/home/arif/Documents/Data/Share_GPT/"
login("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")
#dataset = load_dataset("json", data_files=file_path + 'chat_trainformat_train_master.jsonl')
base_url='https://huggingface.co/datasets/asaeed/chat_training_data/tree/main/'
dataset = load_dataset("json","asaeed/chat_training_data",split="train")

with open("chat_final.jsonl", 'w') as f:
    for record in dataset['train']:
        save_record = {'instruction': record['instruction'], 'input':record['context'],'output': record['response']} 
        f.write(json.dumps(save_record) + "\n")
f.close()

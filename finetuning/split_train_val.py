import random

full_path = "./finetuning/dataset/full.jsonl"
train_path = "./finetuning/dataset/train.jsonl"
val_path = "./finetuning/dataset/val.jsonl"

# Load the dataset
dataset=[]
with open(full_path, 'r', encoding='utf-8') as f:
    for line in f:
        dataset.append(line)
    f.close()

# Shuffle the dataset
random.seed(42)
random.shuffle(dataset)

# Split the dataset to train dataset and validation dataset, 80% for training and 20% for validation
train_size = int(0.8 * len(dataset))
train_dataset = dataset[:train_size]
val_dataset = dataset[train_size:]

# Save the train dataset
with open(train_path, 'w', encoding='utf-8') as f:
    for line in train_dataset:
        f.write(line)
    f.close()

# Save the validation dataset
with open(val_path, 'w', encoding='utf-8') as f:
    for line in val_dataset:
        f.write(line)
    f.close()
import os
import torch
from torch import nn, optim
from torch.utils.data import random_split, DataLoader
from src.data.dataset import ImageCaptionDataset, get_collate_fn
from src.data.tokenizer import load_tokenizer
from src.model.decoder import DecoderWithAttention
from src.train.engine import train_model
from src.train.metrics import compute_bleu, compute_rouge
import yaml

# 📖 Chargement de la config
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# 🧠 Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 Training started on {device}")

# 📦 Dataset & Tokenizer
tokenizer = load_tokenizer(config["tokenizer_path"])

from pathlib import Path
import json

# 📖 Chargement des captions alignées (sortie du 04_)
captions_dict_path = config["captions_dict_path"]

with open(captions_dict_path, "r") as f:
    captions_dict = json.load(f)

# ✅ Vérif d’un ID d’image + 5 captions associées
example_id = next(iter(captions_dict))
print(f"📝 Captions associées à {example_id} :")
for cap in captions_dict[example_id]:
    print(" ➤", cap)

# 🔄 Génération des ID augmentés
augmentations = ["", "_aug0", "_aug1", "_aug2"]
full_pairs = []

for image_id, captions in captions_dict.items():
    for suffix in augmentations:
        full_id = image_id + suffix
        for caption in captions:
            full_pairs.append((full_id, caption))



dataset = ImageCaptionDataset(
    pairs=full_pairs,
    features_dir=config["features_dir"],
    tokenizer=tokenizer
)
collate_fn = get_collate_fn(tokenizer)


# 📏 Proportions des splits
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1
total_size = len(dataset)

train_size = int(train_ratio * total_size)
val_size = int(val_ratio * total_size)
test_size = total_size - train_size - val_size  # le reste

# ✂️ Split
train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])
print(f"📊 Split → Train: {len(train_dataset)} | Val: {len(val_dataset)} | Test: {len(test_dataset)}")

# 🧪 DataLoaders

train_loader = DataLoader(train_dataset, batch_size=config["training"]["batch_size"], shuffle=True, num_workers=8, pin_memory=True, collate_fn=collate_fn)
val_loader = DataLoader(val_dataset, batch_size=config["training"]["batch_size"], shuffle=False, num_workers=8, pin_memory=True, collate_fn=collate_fn)
test_loader = DataLoader(test_dataset, batch_size=config["training"]["batch_size"], shuffle=False, num_workers=8, pin_memory=True, collate_fn=collate_fn)


# 🧠 Modèle
# 🧠 Initialisation
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
decoder = DecoderWithAttention(
    attention_dim=config["model"]["attention_dim"],
    embed_dim=config["model"]["embed_dim"],
    decoder_dim=config["model"]["decoder_dim"],
    vocab_size=tokenizer.vocab_size,
    dropout=config["model"]["dropout"]
).to(device)


# ⚙️ Optimiseur & Critère
params = list(decoder.parameters())
optimizer = optim.Adam(params, lr=config["training"]["lr"])
criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)

# 🏋️ Entraînement
train_model(
    decoder=decoder,
    train_loader=train_loader,
    val_loader=val_loader,
    tokenizer=tokenizer,
    criterion=criterion,
    optimizer=optimizer,
    num_epochs=config["training"]["epochs"],
    patience=config["training"]["patience"]
)

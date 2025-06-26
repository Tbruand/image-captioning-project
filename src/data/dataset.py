import torch
from torch.utils.data import Dataset
import numpy as np
from pathlib import Path
import re
from torch.nn.utils.rnn import pad_sequence
from src.data.tokenizer import Tokenizer


def clean_caption(caption):
    caption = caption.lower()
    caption = re.sub(r"[^a-zA-Z0-9'\s]", "", caption)  # garde lettres, chiffres, apostrophes, espaces
    caption = re.sub(r"\s+", " ", caption)
    return caption.strip()

class ImageCaptionDataset(Dataset):
    def __init__(self, pairs, features_dir, tokenizer, max_length=20):
        self.pairs = pairs
        self.features_dir = Path(features_dir)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        image_id, caption = self.pairs[idx]

        # 📦 Chargement des features
        feature_path = self.features_dir / f"{image_id}.pt"
        features = torch.load(feature_path)

        # 🔡 Encodage de la légende
        caption = clean_caption(caption) 
        encoded = self.tokenizer.encode(caption)
        encoded = encoded[:self.max_length]  # 🔪 Troncature
        encoded_tensor = torch.tensor(encoded, dtype=torch.long)

        return features, encoded_tensor


def get_collate_fn(tokenizer):
    def collate_fn(batch):
        features, captions = zip(*batch)
        features = torch.stack(features)
        lengths = [len(cap) for cap in captions]
        captions_padded = pad_sequence(captions, batch_first=True, padding_value=tokenizer.pad_token_id)
        return features, captions_padded, lengths
    return collate_fn

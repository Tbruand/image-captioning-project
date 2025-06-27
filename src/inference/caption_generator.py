import torch
from PIL import Image
from pathlib import Path
import sys 
project_root = Path(__file__).resolve().parents[2]  # <- remonte jusqu'à la racine
sys.path.append(str(project_root))

from src.model.decoder import DecoderWithAttention
from src.model.encoder import Encoder
from src.data.tokenizer import load_tokenizer
from src.translation.translator import translate_caption
import torch.nn.functional as F


class CaptionGenerator:
    def __init__(self, decoder_path: str, tokenizer_path: str, device=None):
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        tokenizer_full_path = project_root / tokenizer_path
        self.tokenizer = load_tokenizer(str(tokenizer_full_path))

        self.decoder = DecoderWithAttention(
            attention_dim=256,
            embed_dim=256,
            decoder_dim=512,
            vocab_size=len(self.tokenizer.word2idx),
            dropout=0.5
        )
        decoder_full_path = project_root / decoder_path
        self.decoder.load_state_dict(torch.load(decoder_full_path, map_location=self.device))
        self.decoder = self.decoder.to(self.device).eval()

        self.encoder = Encoder().to(self.device).eval()

    def preprocess(self, image: Image.Image):
        features = self.encoder(image).unsqueeze(0).to(self.device)
        return features

    def generate(self, image: Image.Image, max_len: int = 20, translate: bool = False):
        features = self.preprocess(image)
        decoder = self.decoder
        tokenizer = self.tokenizer

        inputs = torch.tensor([[tokenizer.start_token_id]]).to(self.device)
        hidden, cell = decoder.init_hidden_state(features)

        sampled_ids = []
        confidences = []

        for _ in range(max_len):
            embeddings = decoder.embedding(inputs).squeeze(1)
            context, _ = decoder.attention(features, hidden)
            decoder_input = torch.cat([embeddings, context], dim=1)

            hidden, cell = decoder.decode_step(decoder_input, (hidden, cell))
            preds = decoder.fc(hidden)
            probs = F.softmax(preds, dim=1)

            predicted = preds.argmax(1)
            confidence = probs[0, predicted.item()].item()

            sampled_ids.append(predicted.item())
            confidences.append(confidence)

            if predicted.item() == tokenizer.end_token_id:
                break

            inputs = predicted.unsqueeze(1)

        words = [
            tokenizer.idx2word[idx]
            for idx in sampled_ids
            if idx not in {tokenizer.start_token_id, tokenizer.end_token_id, tokenizer.pad_token_id}
        ]
        filtered_conf = [
            conf for idx, conf in zip(sampled_ids, confidences)
            if idx not in {tokenizer.start_token_id, tokenizer.end_token_id, tokenizer.pad_token_id}
        ]

        caption = " ".join(words)

        if translate:
            caption = translate_caption(caption)

        return caption, filtered_conf
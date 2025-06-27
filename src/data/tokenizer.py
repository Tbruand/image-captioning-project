# ✅ Classe Tokenizer (doit être définie avant pickle.load)
class Tokenizer:
    def __init__(self, word2idx):
        self.word2idx = word2idx
        self.idx2word = {idx: word for word, idx in word2idx.items()}

        self.pad_token = "<pad>"
        self.start_token = "<start>"
        self.end_token = "<end>"
        self.unk_token = "<unk>"

        self.pad_token_id = self.word2idx[self.pad_token]
        self.start_token_id = self.word2idx[self.start_token]
        self.end_token_id = self.word2idx[self.end_token]
        self.unk_token_id = self.word2idx[self.unk_token]

        self.vocab_size = len(self.word2idx)

    def encode(self, caption, add_special_tokens=True):
        tokens = caption.strip().split()
        token_ids = [self.word2idx.get(token, self.unk_token_id) for token in tokens]

        if add_special_tokens:
            return [self.start_token_id] + token_ids + [self.end_token_id]
        else:
            return token_ids

    def decode(self, token_ids, remove_special_tokens=True):
        words = [self.idx2word.get(idx, self.unk_token) for idx in token_ids]
        if remove_special_tokens:
            words = [w for w in words if w not in [self.pad_token, self.start_token, self.end_token]]
        return " ".join(words)

import pickle

def load_tokenizer(path):
    with open(path, "rb") as f:
        word2idx = pickle.load(f)
    return Tokenizer(word2idx)

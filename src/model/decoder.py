import torch
import torch.nn as nn
from src.model.attention import Attention


class DecoderWithAttention(nn.Module):
    def __init__(self, attention_dim, embed_dim, decoder_dim, vocab_size, encoder_dim=2048, dropout=0.5):
        super(DecoderWithAttention, self).__init__()
        self.attention = Attention(encoder_dim, decoder_dim, attention_dim)

        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.dropout = nn.Dropout(dropout)
        self.decode_step = nn.LSTMCell(embed_dim + encoder_dim, decoder_dim, bias=True)
        self.init_h = nn.Linear(encoder_dim, decoder_dim)
        self.init_c = nn.Linear(encoder_dim, decoder_dim)
        self.f_beta = nn.Linear(decoder_dim, encoder_dim)
        self.sigmoid = nn.Sigmoid()
        self.fc = nn.Linear(decoder_dim, vocab_size)

        self.init_weights()

    def init_weights(self):
        """Initialisation des poids"""
        self.embedding.weight.data.uniform_(-0.1, 0.1)
        self.fc.bias.data.fill_(0)
        self.fc.weight.data.uniform_(-0.1, 0.1)

    def init_hidden_state(self, encoder_out):
        """Initialise h et c à partir des features encodées"""
        h = self.init_h(encoder_out)  # [batch_size, decoder_dim]
        c = self.init_c(encoder_out)
        return h, c

    def forward(self, encoder_out, encoded_captions, caption_lengths):
        """
        encoder_out: [batch_size, encoder_dim]           → Features extraites
        encoded_captions: [batch_size, max_len]          → Captions target
        caption_lengths: [batch_size] ou [batch_size, 1] → Longueur réelle

        returns:
            - prédictions (logits)
        """
        batch_size = encoder_out.size(0)
        vocab_size = self.fc.out_features

        # 🔐 Sécurité : conversion caption_lengths en Tensor si nécessaire
        if isinstance(caption_lengths, list):
            caption_lengths = torch.tensor(caption_lengths, dtype=torch.long, device=encoder_out.device)
        if caption_lengths.dim() == 2:  # Si [batch_size, 1], on squeeze
            caption_lengths = caption_lengths.squeeze(1)

        embeddings = self.embedding(encoded_captions)  # [batch_size, max_len, embed_dim]
        h, c = self.init_hidden_state(encoder_out)     # h, c : [batch_size, decoder_dim]

        decode_lengths = (caption_lengths - 1).tolist()
        predictions = torch.zeros(batch_size, max(decode_lengths), vocab_size).to(encoder_out.device)

        for t in range(max(decode_lengths)):
            batch_size_t = sum([l > t for l in decode_lengths])
            attn_weighted_encoding, _ = self.attention(encoder_out[:batch_size_t], h[:batch_size_t])

            input_lstm = torch.cat([embeddings[:batch_size_t, t, :], attn_weighted_encoding], dim=1)
            h, c = self.decode_step(input_lstm, (h[:batch_size_t], c[:batch_size_t]))  # LSTMCell

            preds = self.fc(self.dropout(h))  # [batch_size_t, vocab_size]
            predictions[:batch_size_t, t, :] = preds

        return predictions
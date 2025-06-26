import torch
import torch.nn as nn

class Attention(nn.Module):
    def __init__(self, encoder_dim, decoder_dim, attention_dim):
        super(Attention, self).__init__()
        self.encoder_att = nn.Linear(encoder_dim, attention_dim)
        self.decoder_att = nn.Linear(decoder_dim, attention_dim)
        self.full_att = nn.Linear(attention_dim, 1)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, encoder_out, decoder_hidden):
        """
        encoder_out: [batch_size, encoder_dim]     → features encodées
        decoder_hidden: [batch_size, decoder_dim]  → état caché courant du LSTM

        returns:
            - attention_weighted_encoding: [batch_size, encoder_dim]
            - alpha: [batch_size, 1]
        """
        att1 = self.encoder_att(encoder_out)             # [batch_size, attention_dim]
        att2 = self.decoder_att(decoder_hidden)          # [batch_size, attention_dim]
        att = self.full_att(self.relu(att1 + att2))      # [batch_size, 1]
        alpha = self.softmax(att)                        # [batch_size, 1]
        attention_weighted_encoding = encoder_out * alpha  # [batch_size, encoder_dim]
        return attention_weighted_encoding, alpha
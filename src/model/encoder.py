# src/model/encoder.py

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

class Encoder(nn.Module):
    def __init__(self):
        super().__init__()
        # ⚙️ Charger ResNet50 pré-entraîné, sans la couche fully connected (fc)
        resnet = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        self.resnet = nn.Sequential(*list(resnet.children())[:-1])
        self.resnet.eval()
        for param in self.resnet.parameters():
            param.requires_grad = False

        # 🧪 Prétraitement intégré
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    def forward(self, image: Image.Image):
        image_tensor = self.transform(image).unsqueeze(0)
        image_tensor = image_tensor.to(next(self.resnet.parameters()).device)

        with torch.no_grad():
            features = self.resnet(image_tensor)  # (1, 2048, 1, 1)
            features = features.squeeze()         # (2048,)

        return features

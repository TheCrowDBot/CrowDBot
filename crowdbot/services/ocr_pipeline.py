import json

import numpy as np
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F

from crowdbot.services.ocr_preprocessing import crop_rotated, preprocess_for_ocr, TARGET_W, TARGET_H
from crowdbot.config.settings import (
    SHOW_IMAGE_DEFAULT,
    SHOW_LOGS_DEFAULT,
    AUTO_ADVANCE_DEFAULT,
    OCR_LOG_PREFIX,
    IMAGE_PREVIEW_WIDTH,
    OCR_CLASSES,
)

BLANK_IDX = 0


def load_vocab(vocab_path: str):
    with open(vocab_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    characters = data["characters"]
    vocab_size = len(characters)
    idx_to_char = {i + 1: c for i, c in enumerate(characters)}
    return idx_to_char, vocab_size


def decode_predictions(log_probs: torch.Tensor, idx_to_char: dict) -> list[str]:
    pred_indices = torch.argmax(log_probs, dim=-1)  
    results = []
    for seq in pred_indices:
        seq = seq.tolist()
        collapsed = []
        prev = None
        for idx in seq:
            if idx != prev and idx != BLANK_IDX:
                collapsed.append(idx)
            prev = idx
        results.append("".join(idx_to_char.get(i, "") for i in collapsed))
    return results


class CRNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 64, 3, padding=1), nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, 3, padding=1), nn.ReLU(inplace=True),
            nn.BatchNorm2d(256),
            nn.Conv2d(256, 256, 3, padding=1), nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 1), (2, 1)),
            nn.Conv2d(256, 512, 3, padding=1), nn.ReLU(inplace=True),
            nn.BatchNorm2d(512),
            nn.MaxPool2d((2, 1), (2, 1)),
        )
        with torch.no_grad():
            dummy = torch.zeros(1, 1, TARGET_H, TARGET_W)
            out = self.cnn(dummy)
            _, c, h, w = out.shape
            feat_dim = c * h

        self.rnn = nn.LSTM(
            input_size=feat_dim, hidden_size=256, num_layers=1,
            batch_first=True, bidirectional=True, dropout=0.0,
        )
        self.dropout1 = nn.Dropout(0.35)
        self.rnn2 = nn.LSTM(
            input_size=512, hidden_size=256, num_layers=1,
            batch_first=True, bidirectional=True, dropout=0.0,
        )
        self.dropout2 = nn.Dropout(0.35)
        self.fc = nn.Linear(512, num_classes)

    def forward(self, x):
        x = self.cnn(x)
        b, c, h, w = x.shape
        x = x.permute(0, 3, 1, 2)
        x = x.reshape(b, w, c * h)
        x, _ = self.rnn(x)
        x = self.dropout1(x)
        x, _ = self.rnn2(x)
        x = self.dropout2(x)
        logits = self.fc(x)
        return F.log_softmax(logits, dim=-1)


class OCRPipeline:

    def __init__(self, model_path: str, vocab_path: str = "../config/vocab.json", device: str = None):
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        
        torch.backends.cudnn.enabled = False

        self.idx_to_char, vocab_size = load_vocab(vocab_path)
        num_classes = vocab_size + 1  

        self.model = CRNN(num_classes).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

    def run_on_crop(self, crop: np.ndarray) -> str:
        """Corre OCR numa única crop (np.ndarray BGR ou cinza)."""
        tensor = preprocess_for_ocr(crop).to(self.device)
        with torch.no_grad():
            log_probs = self.model(tensor)  # (1, T, C)
        texts = decode_predictions(log_probs.cpu(), self.idx_to_char)
        return texts[0] if texts else ""

    def run(
        self,
        image_path: str,
        schema: dict,
        *,
        show_image=False,
        show_logs=False,
    ):

        img = cv2.imread(image_path)

        for table in schema["tables"]:

            # entity OCR
            entity_crop = crop_rotated(img, table["entity_polygon"])

            table["text"] = self.run_on_crop(entity_crop)

            # attributes OCR
            for attr in table["attributes"]:

                crop = crop_rotated(img, attr["polygon"])

                attr["text"] = self.run_on_crop(crop)

        return schema
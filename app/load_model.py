from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def load_model(model_path, tokenizer_path):
    checkpoint = torch.load(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(
        "wonrax/phobert-base-vietnamese-sentiment")
    model.load_state_dict(checkpoint['model_state_dict'], strict=False)
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    return model, tokenizer

model, tokenizer = load_model(
    model_path = "../train_model/Model/best_checkpoint.pt",
    tokenizer_path = "../train_model/Model/tokeinizer_phobert_base"
)

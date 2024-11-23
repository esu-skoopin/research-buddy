from transformers import LEDTokenizer, LEDForConditionalGeneration
import torch

def load_model(model_dir):
    tokenizer = LEDTokenizer.from_pretrained("allenai/led-base-16384")
    model = LEDForConditionalGeneration.from_pretrained(model_dir)

    # Choose the appropriate device
    device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

    # Move the model to the device
    model.to(device)
    model.eval()

    return model, tokenizer, device

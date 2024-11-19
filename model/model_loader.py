from transformers import LEDTokenizer, LEDForConditionalGeneration
import torch

def load_model(model_dir):
    """
    Loads the fine-tuned model and tokenizer.

    Args:
        model_dir (str): The directory where the fine-tuned model is saved.

    Returns:
        model: The fine-tuned model loaded on the appropriate device.
        tokenizer: The tokenizer associated with the fine-tuned model.
        device: The device (CPU, GPU, or MPS) the model is loaded on.
    """
    # Load the tokenizer
    tokenizer = LEDTokenizer.from_pretrained(model_dir)

    # Load the model
    model = LEDForConditionalGeneration.from_pretrained(model_dir)

    # Determine the device
    device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

    # Move model to the appropriate device
    model.to(device)

    # Set the model to evaluation mode
    model.eval()

    return model, tokenizer, device

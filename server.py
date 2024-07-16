import litserve as ls
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

# Use 'cuda' for NVIDIA GPUs, 'cpu' for non-accelerated
ACCELERATOR = 'cuda'

class HuggingFaceLitAPI(ls.LitAPI):
    def setup(self, device):
        model_name = 'mistralai/Mistral-7B-Instruct-v0.3'

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=ACCELERATOR,
            quantization_config=BitsAndBytesConfig(
                #load_in_8bit=True,        # Use this if you have enough VRAM
                load_in_4bit=True,         # Used this for my 12 GB setup
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16            
            )
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left")
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def decode_request(self, request):
        # Extract text from request
        # This assumes the request payload is of the form: {'text': 'Your input text here'}
        return request["text"]

    def predict(self, text):
        input_ids = self.tokenizer(text, return_tensors="pt").input_ids
        input_ids = input_ids.to(ACCELERATOR)
        return self.model.generate(input_ids, max_new_tokens=1000, pad_token_id=self.tokenizer.eos_token_id)

    def encode_response(self, output):
        # Format the output from the model to send as a response
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

if __name__ == "__main__":
    # Create an instance of your API
    api = HuggingFaceLitAPI()
    # Start the server, specifying the port
    server = ls.LitServer(api, accelerator=ACCELERATOR, timeout=120)
    server.run(port=8000)

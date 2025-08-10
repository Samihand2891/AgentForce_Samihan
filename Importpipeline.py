from transformers import pipeline
import torch

# Create a text-generation pipeline, loading the chosen model
# device_map="auto" intelligently uses a GPU if available
planner_pipeline = pipeline(
    "text-generation",
    model="google/gemma-2b-it",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
    use_auth_token=True,
)
output= planner_pipeline("Explain Ai in simple terms" , max_new_tokens=100)
print(output[0]["generated_text"])








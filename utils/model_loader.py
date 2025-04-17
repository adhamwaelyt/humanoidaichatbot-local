import os
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from ctransformers import AutoModelForCausalLM as CTransformersModel

def is_gguf(model_path):
    return any(f.endswith(".gguf") for f in os.listdir(model_path))

def load_model(model_path):
    if is_gguf(model_path):
        print("🧠 Loading GGUF model locally via ctransformers...")
        return GGUF_wrapper(model_path)
    else:
        print("🔗 Loading Hugging Face model via transformers...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path)
        return pipeline("text-generation", model=model, tokenizer=tokenizer)

def GGUF_wrapper(model_path):
    import multiprocessing
    num_threads = multiprocessing.cpu_count()

    model_file = next((f for f in os.listdir(model_path) if f.endswith(".gguf")), None)
    full_path = os.path.join(model_path, model_file)

    model = CTransformersModel.from_pretrained(
        full_path,
        model_type="llama",  # or "mistral" etc.
        temperature=0.7,
        max_new_tokens=512,
    )

    return lambda prompt, **kwargs: [{"generated_text": model(prompt)}]


from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

# Global variable to cache the pipeline so we don't reload the 1.5B model on every query!
_sql_pipeline = None

def setup_sql_model():
    """Initializes the Qwen model and caches it in memory."""
    global _sql_pipeline
    
    # If it's already loaded, just return it
    if _sql_pipeline is not None:
        return _sql_pipeline

    # Using a lightweight, highly capable 1.5B parameter model
    model_id = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
    print(f"Loading {model_id}... (This may take a minute on the first run)")
    
    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # FIX: Added torch.float16 to halve memory usage and removed device_map="auto" to prevent disk offload errors.
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    )

    # Create a text-generation pipeline
    _sql_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=150, # Slightly increased to allow for JOINs
        return_full_text=False
    )
    
    return _sql_pipeline

def generate_sql_response(prompt):
    """
    This is the function the UI and controller import.
    It takes the prompt, formats it for Qwen, and returns the raw string output.
    """
    # 1. Ensure the model is loaded
    pipe = setup_sql_model()
    
    # 2. Wrap the prompt in Qwen's specific ChatML format for best instruction-following
    formatted_prompt = f"""<|im_start|>system
You are a database assistant. Generate only the raw SQL query for the given schema. Do not explain the code.<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
"""
    
    # 3. Generate the response
    print("\n[🧠] Qwen is processing the query...")
    output = pipe(formatted_prompt)
    
    # 4. Return just the text portion
    return output[0]['generated_text'].strip()

def generate_rag_response(context, question):
    """
    Takes a chunk of text from a PDF and asks the AI to answer a question based ONLY on that text.
    """
    pipe = setup_sql_model() # We reuse the exact same loaded Qwen model in memory!
    
    formatted_prompt = f"""<|im_start|>system
You are a highly intelligent medical assistant. Answer the user's question using ONLY the provided context from the medical document. If the answer is not contained in the context, say "I cannot answer this based on the provided document." Do not use outside knowledge.<|im_end|>
<|im_start|>user
Context:
{context}

Question:
{question}<|im_end|>
<|im_start|>assistant
"""
    print("\n[📚] Qwen is reading the document context...")
    
    # We allow more tokens for RAG answers
    output = pipe(formatted_prompt, max_new_tokens=250)
    
    return output[0]['generated_text'].strip()

if __name__ == "__main__":
    # Quick terminal test to make sure it works standalone
    test_query = "Find all female patients who are older than 40."
    print("Testing generate_sql_response...")
    response = generate_sql_response(test_query)
    print("\n--- Generated Output ---")
    print(response)
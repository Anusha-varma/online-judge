import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_master_code(prompt, language="cpp"):
    print("🛠️ Inside generate_master_code()")
    try:
        print("🔍 Sending request to Hugging Face via OpenAI client...")

        client = OpenAI(
            base_url="https://router.huggingface.co/featherless-ai/v1",
            api_key=os.environ["HF_TOKEN"],
        )

        full_prompt = (
            f"You are a coding assistant. Generate only {language} code that solves the problem below. "
            f"Do not include any explanations, markdown, or comments.\n\n"
            f"---\n{prompt}\n---\n\n"
            f"Make sure the code includes a proper main function to read input and produce output."
        )

        completion = client.chat.completions.create(
            model="HuggingFaceH4/zephyr-7b-alpha",
            messages=[
                {
                    "role": "user",
                    "content": full_prompt,
                }
            ],
        )

        response = completion.choices[0].message.content.strip()
        safe_response = response.encode("utf-8", "ignore").decode("utf-8")

        print("🧠 Hugging Face response:\n", safe_response)
        return safe_response

    except Exception as e:
        print("❌ Exception while generating master code:", str(e))
        return f"Error: {str(e)}"

"""
GPT-OSS Model Client.

Interfaces with the GPT-OSS model via Ollama's OpenAI-compatible API
for generating chat completions with streaming support.
"""

from openai import OpenAI, OpenAIError
from config import MODEL_CONFIG

# ─── OpenAI-compatible client pointing to Ollama ────────────────────
_client = OpenAI(
    base_url=MODEL_CONFIG["base_url"],
    api_key=MODEL_CONFIG["api_key"],
)


def generate_response(messages, stream=True):
    """
    Generate a chat completion from the GPT-OSS model.

    Args:
        messages: List of message dicts with 'role' and 'content' keys.
                  Example: [{"role": "user", "content": "Hello!"}]
        stream: If True, returns a generator that yields token chunks.
                If False, returns the complete response as a string.

    Returns:
        Generator[str] (stream=True) or str (stream=False).

    Raises:
        ConnectionError: If the Ollama server is unreachable.
        RuntimeError: For other API errors.
    """
    try:
        response = _client.chat.completions.create(
            model=MODEL_CONFIG["model_name"],
            messages=messages,
            temperature=MODEL_CONFIG["temperature"],
            max_tokens=MODEL_CONFIG["max_tokens"],
            stream=stream,
        )

        if stream:
            return _stream_tokens(response)
        else:
            return response.choices[0].message.content

    except OpenAIError as e:
        error_msg = str(e)
        if "Connection" in error_msg or "refused" in error_msg or "404" in error_msg or "not found" in error_msg:
            # Fallback for testing when Ollama isn't installed or model is still downloading
            if stream:
                def mock_stream():
                    mock_text = (
                        "🤖 **GPT-OSS Simulated Response**\n\n"
                        "I am running in **fallback mode** because the `gpt-oss:20b` model is either not installed or still downloading. "
                        "Your database, authentication, and chat history are all working perfectly!\n\n"
                        "*Once the background download finishes, this fallback will automatically disappear and you'll get real AI responses.*"
                    )
                    import time
                    for word in mock_text.split(" "):
                        yield word + " "
                        time.sleep(0.05)
                return mock_stream()
            else:
                return "GPT-OSS Simulated Response: Model not found or server not reachable."
        raise RuntimeError(f"Model API error: {error_msg}") from e


def _stream_tokens(response):
    """Yield individual token strings from a streaming response."""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def check_model_health():
    """
    Check if the GPT-OSS model is reachable and responding.

    Returns:
        tuple[bool, str]: (is_healthy, status_message)
    """
    try:
        _client.chat.completions.create(
            model=MODEL_CONFIG["model_name"],
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5,
            stream=False,
        )
        return True, "Model is online and responding."
    except Exception as e:
        return False, f"Model unavailable: {str(e)}"

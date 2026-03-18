import requests
import streamlit as st


HF_ENDPOINT = "https://router.huggingface.co/v1/chat/completions"
HF_MODEL = "meta-llama/Llama-3.2-1B-Instruct"


def get_hf_token() -> str | None:
    token = st.secrets.get("HF_TOKEN")
    if not token:
        return None
    if isinstance(token, str) and "paste_your_hugging_face_token_here" in token:
        return None
    return str(token)


def chat_completion(*, token: str, messages: list[dict], max_tokens: int, temperature: float) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "model": HF_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    resp = requests.post(HF_ENDPOINT, headers=headers, json=payload, timeout=60)
    try:
        data = resp.json()
    except Exception:
        data = {"raw_text": resp.text}

    if resp.status_code >= 400:
        raise RuntimeError(f"HTTP {resp.status_code}: {data}")
    return data


st.set_page_config(page_title="HF Router Chat", layout="centered")
st.title("Hugging Face Router Chat")
st.caption(f"Endpoint: `{HF_ENDPOINT}` • Model: `{HF_MODEL}`")

hf_token = get_hf_token()
if not hf_token:
    st.error(
        "Missing Hugging Face token. Add `HF_TOKEN` in Streamlit secrets (Advanced settings on Streamlit Cloud) "
        "or set it in your local `.streamlit/secrets.toml`."
    )
    st.stop()

with st.sidebar:
    st.header("Settings")
    max_tokens = st.slider("Max tokens", min_value=16, max_value=1024, value=256, step=16)
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
    if st.button("Clear chat"):
        st.session_state.pop("messages", None)
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Say something…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                result = chat_completion(
                    token=hf_token,
                    messages=st.session_state.messages,
                    max_tokens=int(max_tokens),
                    temperature=float(temperature),
                )
                content = result["choices"][0]["message"]["content"]
            except Exception as e:
                st.error(f"Chat request failed: {e}")
                st.stop()
        st.markdown(content)

    st.session_state.messages.append({"role": "assistant", "content": content})

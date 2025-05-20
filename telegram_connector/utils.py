# -*- coding: utf-8 -*-
import json

@staticmethod
def encode_telegram_response(data: dict, ensure_ascii: bool = False) -> str:
    """
    Encode a Python dict (Telegram response) to a JSON string.
    """
    try:
        return json.dumps(data, ensure_ascii=ensure_ascii, indent=2)
    except (TypeError, ValueError) as e:
        print(f"[!] Encoding error: {e}")
        return ""

def extract_telegram_fields(source, mapping):
    """
        The function extracts data from the dict based on the mapping definition.
        Mapping is dict, key is output key, value is tuple: (input_key, default)
    """
    return {
        out_key: source.get(in_key, default)
        for out_key, (in_key, default) in mapping.items()
    }

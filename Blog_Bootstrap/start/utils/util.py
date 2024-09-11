def truncate_text(text, limit=150) -> str:
    if text is not None:
        if len(text) > limit:
            truncated_text = text[:limit] + "...."
        else:
            truncated_text = text
        return truncated_text
    return None

def newline_to_br(text_newline: str) -> str:
    if text_newline is not None:
        return text_newline.replace('\n', '<br>')
    return None
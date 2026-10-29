try:
    import webview

    # Enable file downloading within the PyWebView desktop app window
    webview.settings["ALLOW_DOWNLOADS"] = True
except ImportError:
    # Gracefully ignore when running on Streamlit Cloud or standard web browsers
    pass
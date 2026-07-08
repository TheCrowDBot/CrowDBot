import streamlit as st
from crowdbot.services.model_registry import load_registry, save_registry
from crowdbot.services.model_storage import save_model


class ModelService:

    @staticmethod
    def list_models(model_type: str):
        registry = load_registry()
        return registry.get(model_type, [])

    @staticmethod
    def get_selected(model_type: str):

        registry = load_registry()
        models = registry.get(model_type, [])

        key = f"{model_type}_model_select"
        selected_name = st.session_state.get(key)

        if not models:
            return None

        if not selected_name:
            selected_name = models[0]["name"]
            st.session_state[key] = selected_name

        return next((m for m in models if m["name"] == selected_name), None)

    @staticmethod
    def set_selected(model_type: str, model_name: str):
        st.session_state[f"{model_type}_model_select"] = model_name

    @staticmethod
    def get_active_path(model_type: str):
        model = ModelService.get_selected(model_type)
        return model["path"] if model else None

    @staticmethod
    def upload_model(model_type: str, uploaded_file):

        registry = load_registry()
        path, file_hash = save_model(uploaded_file)

        registry.setdefault(model_type, []).append(
            {
                "name": uploaded_file.name,
                "path": str(path),
                "hash": file_hash,
            }
        )

        save_registry(registry)
        return path

    @staticmethod
    def get_active_vocab_path(model_type: str):
        model = ModelService.get_selected(model_type)
        return model.get("vocab_path") if model else None

    @staticmethod
    def upload_ocr_model(uploaded_model, uploaded_vocab):
        registry = load_registry()
        model_path, model_hash = save_model(uploaded_model)
        vocab_path, _ = save_model(uploaded_vocab)

        registry.setdefault("ocr", []).append(
            {
                "name": uploaded_model.name,
                "path": str(model_path),
                "hash": model_hash,
                "vocab_path": str(vocab_path),
            }
        )

        save_registry(registry)
        return model_path, vocab_path

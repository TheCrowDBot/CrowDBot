import streamlit as st
from pathlib import Path
import time
from datetime import datetime

from crowdbot.config.model_specs import MODEL_SPECS
from crowdbot.config.settings import SUCCESS_MESSAGE_TTL
from crowdbot.services.model_registry import load_registry, save_registry
from crowdbot.services.model_storage import save_model
from crowdbot.services.model_downloader import download_model
from crowdbot.ui.components.temporary_messages import show_temp_success


def _format_ts(ts):
    if not ts:
        return "unknown"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def render_model_manager(model_type: str):
    spec = MODEL_SPECS[model_type]
    registry = load_registry()
    models = registry.get(model_type, [])

    st.subheader(spec["title"])

    pending_key = f"{model_type}_pending_selection"
    select_key = f"{model_type}_model_select"

    if pending_key in st.session_state:
        st.session_state[select_key] = st.session_state.pop(pending_key)
    model_by_name = {m["name"]: m for m in models}

    labels = {
        m["name"]: f"{m['name']} (added {_format_ts(m.get('uploaded_at'))})"
        for m in models
    }

    options = list(labels.values()) + ["Add new model"]

    selected_label = st.selectbox(
        "Select model", options=options, key=f"{model_type}_model_select"
    )

    label_to_name = {v: k for k, v in labels.items()}

    active_key = f"{model_type}_active_path"
    model_path = None

    if selected_label != "Add new model":
        model_name = label_to_name.get(selected_label)
        model_obj = model_by_name.get(model_name)

        if model_obj:
            model_path = model_obj["path"]
            st.session_state[active_key] = model_path

            for extra in spec.get("extra_files", []):
                extra_val = model_obj.get(extra["key"])
                st.session_state[f"{model_type}_{extra['key']}"] = extra_val

            st.success(f"Using {model_name}")
        else:
            st.rerun()

    else:
        uploaded = st.file_uploader(
            f"Upload {model_type} model",
            type=spec["file_type"],
            key=f"{model_type}_upload",
        )

        url = st.text_input(
            spec["url_label"],
            key=f"{model_type}_url",
        )

        if uploaded:
            spec_extras = spec.get("extra_files", [])
            extra_uploads = {}
            all_present = True

            for extra in spec_extras:
                f = st.file_uploader(
                    extra["label"],
                    type=extra["file_type"],
                    key=f"{model_type}_{extra['key']}_upload",
                )
                extra_uploads[extra["key"]] = f
                if extra.get("required") and f is None:
                    all_present = False

            if not all_present:
                st.warning("Faz upload de todos os ficheiros necessários.")

            if st.button(
                "Install uploaded model", key=f"{model_type}_upload_btn", type="primary"
            ):
                path, file_hash = save_model(uploaded, subfolder=spec["folder"])

                entry = {
                    "name": uploaded.name,
                    "path": str(path),
                    "hash": file_hash,
                    "source": "upload",
                    "uploaded_at": time.time(),
                }

                for extra in spec_extras:
                    extra_file = extra_uploads[extra["key"]]
                    if extra_file:
                        extra_path, _ = save_model(extra_file, subfolder=spec["folder"])
                        entry[extra["key"]] = str(extra_path)

                models.append(entry)

                registry[model_type] = models
                save_registry(registry)
                st.session_state[f"{model_type}_pending_selection"] = uploaded.name
                show_temp_success(
                    f"Installed {uploaded.name}",
                    key=f"{model_type}_upload_msg",
                    ttl=SUCCESS_MESSAGE_TTL,
                )

                st.rerun()

        if url:
            if st.button("Download model", key=f"{model_type}_url_btn"):
                with st.spinner("Downloading model"):
                    path, file_hash, name = download_model(
                        url=url, target_dir=Path(f"workspace/models/{spec['folder']}")
                    )

                    models.append(
                        {
                            "name": name,
                            "path": str(path),
                            "hash": file_hash,
                            "source": "url",
                            "url": url,
                            "uploaded_at": time.time(),
                        }
                    )

                    registry[model_type] = models
                    save_registry(registry)
                    st.session_state[f"{model_type}_pending_selection"] = name

                    show_temp_success(
                        f"Downloaded {name}",
                        key=f"{model_type}_url_msg",
                        ttl=SUCCESS_MESSAGE_TTL,
                    )

                    st.rerun()

    result = {"model_path": st.session_state.get(active_key)}

    for extra in spec.get("extra_files", []):
        result[extra["key"]] = st.session_state.get(f"{model_type}_{extra['key']}")

    return result

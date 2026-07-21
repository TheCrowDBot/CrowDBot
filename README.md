# CrowDBot

**CrowDBot** is a Streamlit application that turns images of hand-drawn or scanned Entity-Relationship diagrams into `.drawio` files.

It chains together object detection, text recognition and diagram reconstruction into a single configurable pipeline: it detects entities, attributes and relationship markers in an image, reads the text inside them, figures out how everything connects, and generates a ready-to-open draw.io diagram — batching this over a single image, multiple images, or a whole folder.

---

## ✨ Features

- Streamlit UI for running the full pipeline interactively, step-by-step or automatically
- OBB (oriented bounding box) object detection via an Ultralytics YOLO model
- Custom OCR model (CRNN) to read text from detected entities/attributes
- Relationship/path-finding analysis powered by [CrowMatcher](https://github.com/TheCrowDBot/CrowMatcher)
- `.drawio` diagram generation powered by [crawio](https://github.com/TheCrowDBot/CrawIO)
- Model manager: upload a local model or provide a download URL, for both the OBB and OCR models, with a local registry of previously added models
- Confidence / IoU sliders for detection
- Single image, multiple images, or whole-folder processing
- Selectable outputs to save per stage: OBB detections, matcher result, OCR result, `.drawio` diagram

---

## 📦 Installation

```bash
poetry install
```

Run the app:

```bash
poetry run streamlit run crowdbot/main.py
```

---

## 🚀 Quick Example

1. Start the app (`streamlit run crowdbot/main.py`)
2. In the sidebar, add an OBB model (local `.pt` file or URL) and an OCR model
3. Enter an image path or a folder path and click **Load into pipeline**
4. Click **Process** (and, if *Auto Run* is off, **Run next step** for each stage)
5. Check the results/logs, then find the generated `.drawio` file (and any other selected outputs) in `<input_folder>/out`

---

## 🧱 Core Concepts

### Pipeline stages

CrowDBot runs each image through four pipeline stages, in order:

- **OBBPipeline** — runs the YOLO OBB model and returns detected entities, attributes and relationship markers
- **MatcherPipeline** — calls `crowmatcher.process()` to reconstruct tables and relationships from the detections
- **OCRPipeline** — crops each entity/attribute region and runs the CRNN OCR model to extract its text
- **CrawIOPipeline** — parses the matcher result into an ER schema and uses `crawio` to generate the final diagram

### PipelineRunner

```python
PipelineRunner(pipelines)
```

Runs the configured stages in sequence for the current image, advancing the queue to the next image once all stages complete.

### Model manager

Each model type (`obb`, `ocr`) can be added by local upload or download URL. Added models are kept in a local registry so they can be reselected without re-uploading.

---

## 🧠 Processing Pipeline

```
Images (single / multiple / folder)
    ↓
OBB Detection (Ultralytics YOLO)
    ↓
Relationship Matching (CrowMatcher)
    ↓
OCR on entities/attributes (CRNN)
    ↓
Diagram Generation (crawio)
    ↓
.drawio file + optional stage outputs
```

---

## 📤 Output

For each processed image, CrowDBot can save (configurable via the sidebar's *Output Settings*):

- `<image>_obb.json` — raw detections
- `<image>_matcher.json` — reconstructed tables/relationships
- `<image>_ocr.json` — matcher result enriched with recognized text
- `<image>.drawio` — the final diagram, ready to open in [diagrams.net](https://app.diagrams.net)

Outputs are written to `<input_folder>/out`.

---

## ⚙️ Development

```bash
poetry install
```

Format:

```bash
poe format
```

Lint:

```bash
poe lint
```

Typecheck:

```bash
poe typecheck
```

---

## 📁 Project Structure

crowdbot/
├── main.py
├── config/          # settings, constants, model specs, vocab
├── services/        # pipeline stages, model registry/storage/downloader, image loading
└── ui/
    ├── pages/        # processing page
    ├── sections/     # OBB / OCR model sections
    └── components/   # sidebar, folder selector, pipeline view, model manager

---

## 🧪 Use Cases

- Digitizing hand-drawn or whiteboard ER diagrams into editable draw.io files
- Bulk-converting scanned diagram images from a folder
- Building/labelling datasets for entity, attribute and relationship detection
- Bridging sketches → structured schema → clean diagram, using CrowMatcher and crawio together

---

## 👥 Authors

- Rúben Costa
- Miguel Dias
# CrowDBot – User Story and Functional Requirements

## Epic

As an engineer or annotation specialist, I want to process one or multiple images through a configurable AI pipeline so that I can detect objects, extract text, establish relationships between detected entities, and automatically generate XML files following a custom schema.

---

# User Story

**As a user of CrowDBot, I want to select individual images, multiple images, or an entire directory and process them through configurable detection and OCR models so that I can automatically generate XML files describing the relationships between detected objects and extracted text.**

---

# Description

CrowDBot is a Streamlit application that performs a sequential image-processing workflow consisting of:

1. Image input selection.
2. OBB object detection using an Ultralytics pretrained model.
3. Region extraction from detected objects.
4. OCR using a custom OCR model.
5. Relationship/path-finding analysis.
6. XML generation using a custom schema.
7. Exporting results and logs.

Path-finding may execute concurrently with OCR whenever possible to improve overall processing efficiency.

---

# Workflow

```
Images
    ↓
OBB Detection Model
(Ultralytics)
    ↓
Detected Regions
    ↓
OCR Model
(Custom)
    ↓
Relationship Builder
(Path-Finding)
    ↓
Custom XML Generation
    ↓
Results Export
```

---

# Model Configuration

Before processing images, users must configure:

### OBB Detection Model

The user shall be able to:

* Select a local `.pt` model file.
* Provide a URL to download a model.
* Create a local working copy inside the Streamlit workspace.
* Replace existing models.
* Configure:

  * Confidence threshold.
  * IoU threshold.

### OCR Model

The user shall be able to:

* Select a local model.
* Provide a URL to download the model.
* Copy the model into the Streamlit working directory.
* Replace existing OCR models.

---

# Image Input

Users shall be able to process:

* A single image.
* Multiple images.
* An entire directory.

Supported formats include:

* JPG
* JPEG
* PNG
* TIFF
* BMP

---

# Processing Pipeline

For each image:

1. Execute OBB detection using the selected Ultralytics model.
2. Crop or isolate detected regions.
3. Perform OCR using the configured OCR model.
4. Execute relationship/path-finding logic to establish connections between entities.
5. Generate one XML file using a custom schema.
6. Save outputs.

---

# Relationship Builder

The path-finding stage shall:

* Build relationships among detected entities.
* Associate OCR information with corresponding objects.
* Produce data required for XML generation.
* Run concurrently with OCR when possible.

---

# XML Generation

The system shall:

* Generate one XML file per image.
* Follow a custom XML schema.
* Preserve all object relationships and OCR information.

---

# Optional Visualization

Users may enable or disable:

### Detection Preview

Display:

* Bounding boxes.
* Labels.
* Confidence scores.

### OCR Preview

Display:

* Extracted text.
* Associated regions.

### XML Preview

Display:

* Generated XML content.

### Logs

Display:

* Processing status.
* Errors.
* Execution information.

---

# Export Options

## XML Export

Users shall be able to:

* Save XML files to a selected directory.
* Download XML files individually.

## ZIP Export

Users shall be able to download a ZIP package containing:

* Original image.
* Generated XML.
* Processing logs.
* Runtime parameters.
* Detection information.

---

# Streamlit Sections

## Home

Overview of CrowDBot.

## Model Configuration

### OBB Detection Model

* Local file selection.
* URL download.
* Working-directory copy.
* Confidence slider.
* IoU slider.

### OCR Model

* Local file selection.
* URL download.
* Working-directory copy.

## Input Selection

* Single image.
* Multiple images.
* Directory selection.

## Processing

Displays:

* Current image.
* Progress bar.
* Status messages.

## Results

Optional tabs:

* Detection results.
* OCR results.
* XML preview.
* Logs.

## Export

* Save XMLs.
* Download XML.
* Download ZIP package.

---

# Acceptance Criteria

### AC-1 Image Input

Given the application is running,

When the user selects a file, multiple files, or a directory,

Then CrowDBot shall load all supported images.

---

### AC-2 OBB Model Configuration

Given the user needs an OBB model,

When they select a local model or provide a URL,

Then CrowDBot shall create a working copy inside its local workspace.

---

### AC-3 OCR Model Configuration

Given the user needs an OCR model,

When they select a local model or provide a URL,

Then CrowDBot shall create a working copy inside its local workspace.

---

### AC-4 Detection Parameters

Given a configured OBB model,

When the user modifies confidence and IoU thresholds,

Then the selected values shall be used during inference.

---

### AC-5 Sequential Processing

Given images are loaded,

When processing starts,

Then images shall be processed sequentially.

---

### AC-6 Relationship Analysis

Given detection and OCR results are available,

When path-finding executes,

Then relationships among entities shall be established.

---

### AC-7 XML Generation

Given processing is completed,

When an image finishes processing,

Then one XML file shall be generated for that image.

---

### AC-8 Visualization

Given optional previews are enabled,

When processing finishes,

Then users shall be able to view detection results, OCR output, XML, and logs.

---

### AC-9 Export

Given processing results exist,

When the user requests export,

Then CrowDBot shall provide:

* XML files.
* ZIP packages containing images, XML files, logs, and runtime parameters.

---

# Non-Functional Requirements

* Built with Streamlit.
* Uses Ultralytics for OBB detection.
* Supports local and URL-based model provisioning.
* Maintains local copies of all models.
* Supports batch image processing.
* Sequential execution with concurrent OCR and path-finding where applicable.
* Modular architecture for future pipeline extensions.
* Robust error handling and logging.

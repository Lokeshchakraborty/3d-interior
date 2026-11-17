# Graph Report - interiormodel  (2026-11-17)

## Corpus Check
- 110 files · ~436,601 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: .example 1, (none) 1, .zip 1)

## Summary
- 32 nodes · 39 edges · 6 communities (4 shown, 2 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.9)
- Token cost: 1,250 input · 1,420 output

## Community Hubs (Navigation)
- LoRA Training & Architecture
- Flask Backend & Streaming
- ZeroGPU Cloud Inference
- Project Report PDF Generator
- Interactive Web UI Client
- Dataset Curation Pipeline

## God Nodes (most connected - your core abstractions)
1. `redesign()` - 6 edges
2. `NumberedCanvas` - 5 edges
3. `4-Bit QLoRA Fine-Tuning (PEFT)` - 4 edges
4. `Hugging Face Space API (lokesh006/room-design-api)` - 4 edges
5. `displayFilePreview()` - 3 edges
6. `build_pdf()` - 2 edges
7. `get_client()` - 2 edges
8. `index()` - 2 edges
9. `showStatus()` - 2 edges
10. `clearStatus()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `redesign()` --calls--> `Hugging Face Space API (lokesh006/room-design-api)`  [EXTRACTED]
  server.py → AI_Interior_Redesign_Project_Report.pdf
- `Hugging Face Space API (lokesh006/room-design-api)` --references--> `Trained LoRA Weights (safetensors)`  [EXTRACTED]
  AI_Interior_Redesign_Project_Report.pdf → pytorch_lora_weights.safetensors
- `build_pdf()` --implements--> `Executive Summary & Hardware Challenge`  [EXTRACTED]
  generate_project_pdf.py → AI_Interior_Redesign_Project_Report.pdf
- `4-Bit QLoRA Fine-Tuning (PEFT)` --references--> `Interior LoRA Dataset Pairs (50 Samples)`  [EXTRACTED]
  AI_Interior_Redesign_Project_Report.pdf → interior_lora_dataset.zip
- `Trained LoRA Weights (safetensors)` --conceptually_related_to--> `4-Bit QLoRA Fine-Tuning (PEFT)`  [EXTRACTED]
  pytorch_lora_weights.safetensors → AI_Interior_Redesign_Project_Report.pdf

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **LoRA Dataset & Training Flow** — prepare_dataset, report_trigger_word_token, dataset_interior_lora_archive, weights_pytorch_lora_weights [EXTRACTED 0.95]
- **Distributed ZeroGPU Client-Server Flow** — templates_index_html_ui, static_app, server_redesign, report_hf_space_api, report_zerogpu_serverless [EXTRACTED 0.95]

## Communities (6 total, 2 thin omitted)

### Community 0 - "LoRA Training & Architecture"
Cohesion: 0.25
Nodes (7): Interior LoRA Dataset Pairs (50 Samples), FLUX.2 Klein Base 4B MMDiT, LoRA Decomposition W = W0 + (alpha/r)*(B*A), 4-Bit QLoRA Fine-Tuning (PEFT), LoRA Trigger Token (modern_interior), Room Redesign Studio Web Interface, Trained LoRA Weights (safetensors)

### Community 1 - "Flask Backend & Streaming"
Cohesion: 0.38
Nodes (6): AI 3D Interior Redesign Overview, Base64 Zero-Disk Streaming Architecture, route, get_client(), index(), redesign()

### Community 2 - "ZeroGPU Cloud Inference"
Cohesion: 0.33
Nodes (4): build_pdf(), Executive Summary & Hardware Challenge, Hugging Face Space API (lokesh006/room-design-api), Hugging Face ZeroGPU Dynamic Allocation

### Community 4 - "Interactive Web UI Client"
Cohesion: 0.60
Nodes (3): clearStatus(), displayFilePreview(), showStatus()

## Knowledge Gaps
- **4 isolated node(s):** `AI 3D Interior Redesign Overview`, `FLUX.2 Klein Base 4B MMDiT`, `LoRA Decomposition W = W0 + (alpha/r)*(B*A)`, `Dataset Curation & Normalization`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 7 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Hugging Face Space API (lokesh006/room-design-api)` connect `ZeroGPU Cloud Inference` to `LoRA Training & Architecture`, `Flask Backend & Streaming`?**
  _High betweenness centrality (0.570) - this node is a cross-community bridge._
- **Why does `redesign()` connect `Flask Backend & Streaming` to `ZeroGPU Cloud Inference`, `Interactive Web UI Client`?**
  _High betweenness centrality (0.535) - this node is a cross-community bridge._
- **What connects `AI 3D Interior Redesign Overview`, `FLUX.2 Klein Base 4B MMDiT`, `LoRA Decomposition W = W0 + (alpha/r)*(B*A)` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
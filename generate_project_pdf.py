import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_PATH = r"c:\Users\LOKESH CHAKRABORTY\Downloads\interiormodel\AI_Interior_Redesign_Project_Report.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Suppress header on cover page
        if self._pageNumber > 1:
            self.drawString(54, 750, "AI-Powered Interior Redesign System | Technical Project Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer on all pages
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "Author: Lokesh Chakraborty | Academic Project Documentation")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0F172A")    # Deep Slate
    c_accent = colors.HexColor("#2563EB")     # Royal Blue
    c_teal = colors.HexColor("#0D9488")       # Teal
    c_body = colors.HexColor("#334155")       # Slate Body Text
    c_card_bg = colors.HexColor("#F8FAFC")    # Light Gray BG
    c_border = colors.HexColor("#E2E8F0")     # Light Border
    
    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_primary,
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_accent,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_body,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=0
    )
    
    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B")
    )
    
    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_primary
    )
    
    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=c_body
    )

    story = []

    # =========================================================================
    # HEADER / TITLE BLOCK
    # =========================================================================
    story.append(Paragraph("AI-Powered Interior Redesign System", title_style))
    story.append(Paragraph("Image-to-Image Generation with Custom Fine-Tuned FLUX.2 Klein (4B) via 4-Bit QLoRA", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=0, spaceAfter=12))
    
    # Metadata Card
    meta_data = [
        [Paragraph("<b>Student Author:</b>", meta_label), Paragraph("Lokesh Chakraborty", meta_val),
         Paragraph("<b>Local Hardware:</b>", meta_label), Paragraph("ASUS Vivobook 16 (i5-12500H, Iris Xe)", meta_val)],
        [Paragraph("<b>Model Architecture:</b>", meta_label), Paragraph("FLUX.2 Klein Base 4B (DiT)", meta_val),
         Paragraph("<b>Fine-Tuning Method:</b>", meta_label), Paragraph("4-Bit QLoRA (NF4) via PEFT", meta_val)],
        [Paragraph("<b>Deployment Platform:</b>", meta_label), Paragraph("Hugging Face ZeroGPU (A100)", meta_val),
         Paragraph("<b>Local Client Footprint:</b>", meta_label), Paragraph("0 MB VRAM, ~3.5s per image", meta_val)]
    ]
    t_meta = Table(meta_data, colWidths=[120, 140, 110, 134])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 1: EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Problem Formulation", h1_style))
    story.append(Paragraph(
        "Modern architectural and interior visualization typically requires commercial CAD software, manual 3D rendering, "
        "or enterprise-grade cloud compute. The objective of this project was to construct an autonomous, end-to-end "
        "<b>AI-driven Interior Redesign System</b> where an end user uploads an image of an unadorned, empty, or outdated room "
        "and receives a high-resolution (1024×1024), photorealistic redesigned room matching a custom luxury aesthetic.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Core Engineering Challenge:</b> The system had to be developed and operated using a standard consumer ultrabook "
        "(ASUS Vivobook 16 equipped with an Intel Core i5-12500H processor and integrated Intel Iris Xe Graphics). "
        "Because integrated GPUs have <b>0 MB of dedicated Video RAM (VRAM)</b> and lack NVIDIA CUDA acceleration, running or "
        "training modern generative models locally was computationally impossible without system freezing or Out-Of-Memory (OOM) failures. "
        "This project successfully bypassed hardware boundaries by combining <b>Quantized Low-Rank Adaptation (4-bit QLoRA)</b> in the cloud, "
        "automated dataset curation, and a serverless <b>Distributed Cloud Inference Client</b>.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 2: ARCHITECTURAL EVALUATION & MODEL BENCHMARKING
    # =========================================================================
    story.append(Paragraph("2. Architectural Evaluation & Model Selection", h1_style))
    story.append(Paragraph(
        "During research and prototyping, multiple generative diffusion backbones were experimentally tested to determine "
        "which model could best preserve room geometry while synthesizing realistic furniture, lighting, and textures.",
        body_style
    ))
    
    model_table_data = [
        [Paragraph("<b>Model Architecture</b>", meta_label), 
         Paragraph("<b>Model Size</b>", meta_label), 
         Paragraph("<b>VRAM Req.</b>", meta_label), 
         Paragraph("<b>Interior Fidelity & Geometry Assessment</b>", meta_label)],
        [Paragraph("Stable Diffusion 1.5", body_style), Paragraph("~2.1 GB", body_style), Paragraph("4 GB - 6 GB", body_style),
         Paragraph("High speed; but struggles with architectural straight lines and prompt fidelity without ControlNet.", body_style)],
        [Paragraph("Realistic Vision v5.1", body_style), Paragraph("~4.2 GB", body_style), Paragraph("6 GB - 8 GB", body_style),
         Paragraph("Photorealistic textures, but prone to warping wall boundaries in direct img2img mode.", body_style)],
        [Paragraph("<b>FLUX.2 Klein Base (4B)</b><br/><i>(Selected System)</i>", meta_label), 
         Paragraph("~8.2 GB (16-bit)<br/>~2.2 GB (4-bit)", meta_val), 
         Paragraph("~4.5 GB (QLoRA)", meta_val),
         Paragraph("<b>State-of-the-Art</b>: Rectified Flow Transformer (MMDiT) with native multi-reference editing and Qwen text encoder.", meta_val)]
    ]
    t_models = Table(model_table_data, colWidths=[120, 75, 75, 234])
    t_models.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EEF2F6")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_models)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 3: DATASET ENGINEERING & CURATION PIPELINE
    # =========================================================================
    story.append(Paragraph("3. Dataset Engineering & Automated Curation Pipeline", h1_style))
    story.append(Paragraph(
        "Supervised fine-tuning of generative models requires strict image-caption consistency. "
        "A customized data-preparation script (<code>prepare_dataset.py</code>) was developed to autonomously stream, "
        "filter, format, and package 50 ultra-high-resolution indoor living space pairs from Hugging Face datasets.",
        body_style
    ))
    story.append(Paragraph("<b>Pipeline Execution Stages:</b>", h2_style))
    story.append(Paragraph("• <b>Streaming Ingestion:</b> Image streaming from <code>MohamedAli77/interior-rooms</code> and <code>ellljoy/interior-design</code>.", bullet_style))
    story.append(Paragraph("• <b>Smart Center-Cropping:</b> Automatically cropped variable aspect-ratio photographs into strict 1:1 squares using Lanczos resampling to prevent distortion.", bullet_style))
    story.append(Paragraph("• <b>Resolution Normalization:</b> Upscaled/standardized to native 1024×1024 pixel tensors matching FLUX patch requirements.", bullet_style))
    story.append(Paragraph("• <b>Trigger Word Synthesis:</b> Every caption was prepended with a custom trigger keyword: <code>modern_interior</code> (e.g. <i>'modern_interior, living room with white marble floors, white oak coffee table, and warm sunlight'</i>).", bullet_style))
    story.append(Paragraph("• <b>Packaging:</b> Automatically compressed into a 12.1 MB portable archive (<code>interior_lora_dataset.zip</code>) for cloud ingestion.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 4: MATHEMATICAL FOUNDATION & 4-BIT QLoRA TRAINING
    # =========================================================================
    story.append(Paragraph("4. Mathematical Foundation & 4-Bit QLoRA Fine-Tuning", h1_style))
    story.append(Paragraph(
        "Full model fine-tuning of a 4-Billion parameter transformer requires computing gradients and optimizer states for all weights, "
        "demanding over <b>45 GB to 60 GB of VRAM</b> (far exceeding any free GPU tier). "
        "To overcome this, the project implemented <b>Quantized Low-Rank Adaptation (QLoRA)</b>.",
        body_style
    ))
    
    story.append(Paragraph("<b>Mathematical Principle of LoRA:</b>", h2_style))
    story.append(Paragraph(
        "During LoRA adaptation, the pre-trained weight matrix <i>W<sub>0</sub> ∈ ℝ<sup>d × k</sup></i> is frozen and does not receive gradient updates. "
        "Instead, parameter updates are factorized into low-rank decomposition matrices <i>A ∈ ℝ<sup>r × k</sup></i> and <i>B ∈ ℝ<sup>d × r</sup></i>, "
        "where rank <i>r ≪ min(d, k)</i>:",
        body_style
    ))
    
    # Formula Box
    formula_data = [[
        Paragraph("<font size=11><b><i>W = W<sub>0</sub> + ΔW = W<sub>0</sub> + (α / r) · (B · A)</i></b></font><br/>"
                  "<font size=8.5 color='#475569'>Where rank r = 16, scaling factor α = 16, and target projection layers = {to_q, to_k, to_v, to_out}.</font>",
                  callout_style)
    ]]
    t_formula = Table(formula_data, colWidths=[504])
    t_formula.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_formula)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Parameter Efficiency Analysis:</b>", h2_style))
    story.append(Paragraph(
        "During training initialization, the PEFT wrapper confirmed the following parameter reduction:",
        body_style
    ))
    
    param_table = [
        [Paragraph("<b>Metric</b>", meta_label), Paragraph("<b>Full FLUX.2 Base 4B</b>", meta_label), Paragraph("<b>Our Custom LoRA Adapter</b>", meta_label), Paragraph("<b>Efficiency Ratio</b>", meta_label)],
        [Paragraph("Trainable Parameters", body_style), Paragraph("3,877,510,656 params", body_style), Paragraph("<b>1,966,080 params</b>", body_style), Paragraph("<b>99.949% Frozen</b> (Only 0.05% trained!)", body_style)],
        [Paragraph("Disk / Memory Size", body_style), Paragraph("~8.2 GB - 16.0 GB", body_style), Paragraph("<b>8.37 MB (.safetensors)</b>", body_style), Paragraph("<b>1,000× smaller</b> file footprint", body_style)]
    ]
    t_param = Table(param_table, colWidths=[120, 130, 120, 134])
    t_param.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EEF2F6")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_param)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Engineering Breakthroughs in the Training Pipeline:</b>", h2_style))
    story.append(Paragraph("• <b>4-Bit NormalFloat4 (NF4) Quantization:</b> Base DiT weights were quantized to 4-bit using <code>bitsandbytes</code>, shrinking baseline memory from 8.5 GB down to 2.2 GB VRAM.", bullet_style))
    story.append(Paragraph("• <b>Latent Pre-Caching (<code>--cache_latents</code>):</b> All 50 training images were encoded through the VAE once upfront. The VAE model was then unloaded from GPU memory, completely eliminating PCIe memory-swapping bottlenecks and dropping epoch time from hours to minutes.", bullet_style))
    story.append(Paragraph("• <b>8-Bit Adam Optimizer (<code>AdamW8bit</code>):</b> Reduced optimizer memory state from 4 GB down to ~50 MB.", bullet_style))
    story.append(Paragraph("• <b>Gradient Checkpointing:</b> Recomputed activations during the backward pass to maintain low peak VRAM headroom under 5.0 GB on Google Colab's single NVIDIA T4 GPU.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: DISTRIBUTED DEPLOYMENT ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("5. Distributed Client-Server Deployment Architecture", h1_style))
    story.append(Paragraph(
        "To allow the local ASUS Vivobook laptop to redesign rooms with zero local GPU compute, a decoupled client-server architecture was established:",
        body_style
    ))
    
    arch_flow = [
        [Paragraph("<b>Local Client (Vivobook)</b>", meta_label), Paragraph("<b>Secure API Gateway</b>", meta_label), Paragraph("<b>Serverless Cloud Server (Hugging Face)</b>", meta_label)],
        [Paragraph("• User selects local room photo (<code>my_room.jpg</code>)<br/>"
                   "• Formulates style prompt (<code>modern_interior, ...</code>)<br/>"
                   "• Runs lightweight Python script (<code>text_redisgn.py</code>)<br/>"
                   "• <b>Hardware:</b> 0 MB VRAM, ~2% CPU usage", body_style),
         Paragraph("──(HTTPS POST)──><br/><br/>"
                   "Gradio Client RPC<br/>"
                   "Auto-authentication<br/><br/>"
                   "<──(JPEG Response)─", ParagraphStyle('Arrow', parent=code_style, alignment=1)),
         Paragraph("• <b>Hardware:</b> NVIDIA A100 GPU (ZeroGPU)<br/>"
                   "• <b>Core Engine:</b> <code>FLUX.2-klein-4B</code> (BF16)<br/>"
                   "• <b>Custom Adapter:</b> <code>pytorch_lora_weights.safetensors</code><br/>"
                   "• <b>Latency:</b> ~3.5 seconds generation time<br/>"
                   "• <b>Output:</b> 1024×1024 Photorealistic Render", body_style)]
    ]
    t_arch = Table(arch_flow, colWidths=[168, 120, 216])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_card_bg),
        ('BACKGROUND', (0,1), (0,1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (2,1), (2,1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: VERIFICATION & EXPERIMENTAL RESULTS
    # =========================================================================
    story.append(Paragraph("6. Experimental Results & Verification", h1_style))
    story.append(Paragraph(
        "The system was validated through live image-to-image inference runs using test photographs of unrenovated rooms. "
        "The fine-tuned FLUX.2 Klein model demonstrated remarkable performance across three key criteria:",
        body_style
    ))
    story.append(Paragraph("• <b>Structural Integrity:</b> Room perspective, ceiling heights, window placement, and wall orientations from the user's uploaded image were accurately retained.", bullet_style))
    story.append(Paragraph("• <b>Material Realism:</b> The fine-tuned weights successfully introduced high-end Scandinavian finishes including natural light oak hardwood, neutral linen upholstery, marble coffee tables, and organic indoor flora.", bullet_style))
    story.append(Paragraph("• <b>Inference Efficiency:</b> While generating locally would have taken over 20 minutes per image on an Intel CPU, the distributed ZeroGPU pipeline returned verified 1024×1024 JPEG results (<code>flux_redesigned_room.jpg</code>) in <b>under 4 seconds</b>.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: SUMMARY OF PROJECT ARTIFACTS
    # =========================================================================
    story.append(Paragraph("7. Summary of Delivered Project Artifacts", h1_style))
    
    artifact_data = [
        [Paragraph("<b>Artifact Name</b>", meta_label), Paragraph("<b>Type / Location</b>", meta_label), Paragraph("<b>Technical Purpose & Role</b>", meta_label)],
        [Paragraph("<code>prepare_dataset.py</code>", code_style), Paragraph("Python Script", body_style), Paragraph("Streams HF datasets, crops to 1024×1024, injects trigger word, and archives pairs.", body_style)],
        [Paragraph("<code>interior_lora_dataset.zip</code>", code_style), Paragraph("Dataset Archive (12.1 MB)", body_style), Paragraph("50 curated, captioned, and formatted image-caption training pairs.", body_style)],
        [Paragraph("<code>pytorch_lora_weights.safetensors</code>", code_style), Paragraph("LoRA Model (8.37 MB)", body_style), Paragraph("Trained low-rank adapter containing 1.96M interior design weights.", body_style)],
        [Paragraph("<code>app.py</code> (Hugging Face Space)", code_style), Paragraph("Cloud Serverless Backend", body_style), Paragraph("ZeroGPU Gradio endpoint serving FLUX.2 Klein + fine-tuned LoRA on A100.", body_style)],
        [Paragraph("<code>text_redisgn.py</code>", code_style), Paragraph("Local Client Script", body_style), Paragraph("Sends local room photos to cloud and downloads 1024×1024 results in seconds.", body_style)],
        [Paragraph("<code>flux_redesigned_room.jpg</code>", code_style), Paragraph("Output Artifact (250 KB)", body_style), Paragraph("Live verified 1024×1024 redesigned interior room photograph.", body_style)]
    ]
    t_art = Table(artifact_data, colWidths=[160, 110, 234])
    t_art.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EEF2F6")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_art)
    story.append(Spacer(1, 14))

    # Sign-off box
    sign_off = [
        [Paragraph("<b>Conclusion & Academic Assessment:</b><br/>"
                   "This project proves that cutting-edge Generative AI models can be adapted and deployed without high-budget local hardware. "
                   "Through mathematical parameter-efficiency (QLoRA) and cloud-native architecture, enterprise-grade interior architectural design "
                   "was achieved on a lightweight student laptop.", callout_style)]
    ]
    t_sign = Table(sign_off, colWidths=[504])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Professional Project Report PDF successfully compiled at:\n{PDF_PATH}")

if __name__ == "__main__":
    build_pdf()

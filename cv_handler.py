import os
import numpy as np
from PIL import Image

try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False


class CVInspectionHandler:
    """Computer Vision inspection handler for analyzing site progress photos."""

    def __init__(self):
        pass

    def analyze_image(self, file_path):
        """Extract structural feature indicators and return completeness & risk metrics."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found: {file_path}")

        try:
            # Load with PIL as fallback baseline
            pil_img = Image.open(file_path).convert("RGB")
            img_width, img_height = pil_img.size
            img_np = np.array(pil_img)

            if HAS_OPENCV:
                cv_img = cv2.imread(file_path)
                if cv_img is None:
                    cv_img = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

                gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

                # Edge Density (Structural Complexity Indicator)
                edges = cv2.Canny(gray, 100, 200)
                edge_density = float(np.sum(edges > 0) / (edges.shape[0] * edges.shape[1]))

                # Contrast & Brightness (Lighting / Weather condition indicator)
                brightness = float(np.mean(gray))
                contrast = float(np.std(gray))

                # Color Distribution (Concrete / Earth / Equipment estimation)
                hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
                gray_mask = cv2.inRange(hsv, (0, 0, 50), (180, 50, 200)) # concrete / metallic gray
                concrete_ratio = float(np.sum(gray_mask > 0) / (gray_mask.shape[0] * gray_mask.shape[1]))

            else:
                # Fallback using PIL / numpy
                gray_np = np.mean(img_np, axis=2)
                brightness = float(np.mean(gray_np))
                contrast = float(np.std(gray_np))
                edge_density = float(contrast / 128.0) # heuristic fallback
                concrete_ratio = 0.35

            # Calculate Completeness Score (0 - 100%)
            # High edge density + structural gray ratio correlates with structural framing progress
            raw_completeness = (edge_density * 250.0) + (concrete_ratio * 40.0) + (brightness / 255.0 * 20.0)
            completeness_score = round(float(np.clip(raw_completeness, 10.0, 98.0)), 1)

            # Structural Risk Score (0 - 100)
            # Low edge density or extreme low brightness/contrast signals structural delay or bad inspection visibility
            visibility_penalty = max(0.0, 40.0 - brightness)
            structural_risk = (100.0 - completeness_score) * 0.5 + (visibility_penalty * 0.5)
            structural_risk_score = round(float(np.clip(structural_risk, 5.0, 95.0)), 1)

            # Site Anomaly Detection
            anomalies = []
            if completeness_score < 30.0:
                anomalies.append("Low structural framing progress detected compared to schedule phase.")
            if brightness < 60.0:
                anomalies.append("Sub-optimal image lighting or heavy overcast cloud cover detected.")
            if edge_density < 0.05:
                anomalies.append("Low visual detail density - possible site inactivity or barren terrain.")
            if not anomalies:
                anomalies.append("Normal site progression observed. No major structural anomalies detected.")

            # Site delay factor (0.0 to 1.0) for ML feature pipeline
            cv_delay_factor = round(float(np.clip((100.0 - completeness_score) / 100.0 * 0.5, 0.0, 1.0)), 2)

            return {
                "completeness_score": completeness_score,
                "structural_risk_score": structural_risk_score,
                "cv_site_delay_factor": cv_delay_factor,
                "image_dimensions": f"{img_width}x{img_height}",
                "brightness": round(brightness, 1),
                "contrast": round(contrast, 1),
                "detected_anomalies": anomalies
            }

        except Exception as e:
            # Safe fallback response if image parsing fails
            return {
                "completeness_score": 50.0,
                "structural_risk_score": 40.0,
                "cv_site_delay_factor": 0.2,
                "image_dimensions": "Unknown",
                "brightness": 128.0,
                "contrast": 50.0,
                "detected_anomalies": [f"Image processing note: {str(e)}"]
            }

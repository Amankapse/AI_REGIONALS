import cv2
import numpy as np
from ultralytics import YOLO
import torch

class VisionModel:
    def __init__(self, model_path="yolov8n.pt"):
        print(f"[VisionModel] Loading {model_path}...")
        self.model = YOLO(model_path)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"[VisionModel] Using device: {self.device}")
    
    def predict(self, image_bytes):
        # Decode bytes → image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return {"detections": [], "meta": {"confidence_avg": 0, "model_version": "v1.0"}}
        
        # Preprocess for YOLO (resize, normalize)
        img_resized = cv2.resize(img, (640, 640))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # YOLO inference with device specification
        results = self.model(img_rgb, conf=0.35, verbose=False, device=self.device)
        
        detections = []
        for r in results:
            if r.boxes is not None and len(r.boxes) > 0:
                boxes = r.boxes  # Tensor with xyxy, conf, cls
                
                for box in boxes:
                    # Robust tensor → float conversion
                    cls_id = int(box.cls.item())
                    conf = float(box.conf.item())
                    xyxy = box.xyxy[0].cpu().numpy().tolist()
                    
                    # Filter low confidence
                    if conf < 0.35:
                        continue
                    
                    # Scale bbox back to original image dimensions
                    orig_h, orig_w = img.shape[:2]
                    scale_x = orig_w / 640
                    scale_y = orig_h / 640
                    
                    x1, y1, x2, y2 = xyxy
                    x1 *= scale_x
                    y1 *= scale_y
                    x2 *= scale_x
                    y2 *= scale_y
                    
                    # Convert bbox to [x, y, w, h] - center top-left
                    x = int(x1)
                    y = int(y1)
                    w = int(x2 - x1)
                    h = int(y2 - y1)
                    
                    # Manufacturing defect severity mapping (customize for your needs)
                    defect_type = self.model.names[cls_id]
                    severity = self._get_defect_severity(defect_type, conf)
                    
                    detections.append({
                        "type": defect_type,
                        "confidence": conf,
                        "bbox": [x, y, w, h],
                        "severity": severity,
                        "area_ratio": (w * h) / (orig_w * orig_h)
                    })
        
        conf_avg = np.mean([d["confidence"] for d in detections]) if detections else 0
        print(f"[VisionModel] Detected {len(detections)} defects, avg conf: {conf_avg:.2f}")
        
        return {
            "detections": detections,
            "meta": {
                "confidence_avg": float(conf_avg),
                "model_version": "v1.1",
                "total_defects": len(detections),
                "device": self.device,
                "image_shape": img.shape
            }
        }
    
    def _get_defect_severity(self, defect_type, confidence):
        """Map defect types to severity levels for manufacturing quality control"""
        severity_map = {
            'missing_hole': 'HIGH' if confidence > 0.7 else 'MEDIUM',
            'mouse_bite': 'HIGH',
            'open_circuit': 'CRITICAL',
            'short': 'CRITICAL',
            'spur': 'MEDIUM',
            'spurious_copper': 'MEDIUM',
            # Add IPC-A-610 specific defect mappings
        }
        return severity_map.get(defect_type.lower(), "LOW")


# Global export for production use
vision_model_instance = VisionModel("yolov8n.pt")

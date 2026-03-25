import numpy as np
import tensorflow as tf
from app import load_model, generate_gradcam_plus_plus # Assuming app.py is structurally sound enough to import

try:
    from app import load_model, generate_gradcam_plus_plus
    load_model()
    import app
    model = app.model
    # Dummy input
    img_array = np.random.rand(1, 224, 224, 3).astype(np.float32)
    # Target class arbitrary
    class_idx = 0
    print("Testing generate_gradcam_plus_plus...")
    cam = generate_gradcam_plus_plus(img_array, model, class_idx)
    if cam is None:
        print("CAM is None!")
    else:
        print(f"CAM shape: {cam.shape}")
except Exception as e:
    import traceback
    traceback.print_exc()

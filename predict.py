from ultralytics import YOLO

# Load a model
model = YOLO("/home/image2/workspace/jjh/smoke_detect/runs/detect/train18/weights/last.pt")  #

# Use the model
model.predict(source="test_image_other", save=True, save_txt=True, conf=0.1, name='baseline_test_other_best1')  # train the model



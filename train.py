from ultralytics import YOLO

# Load a model
model = YOLO("yolov8m.yaml")  # build a new model from scratch

# Use the model
model.train(data="smoke.yaml", epochs=300, name="DCNv3", device=0)  # train the model
metrics = model.val()  # evaluate model performance on the validation set



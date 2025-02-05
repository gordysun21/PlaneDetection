from ultralytics import YOLO

model = YOLO('yolov8n.pt')

model.train(
    data='yolo_dataset/dataset.yaml',
    epochs=50,
    batch=16,
    imgsz=640,
    device='cpu'
)

model.export(format='onnx')
results = model('yolostuff/test.jpg')
results.show()

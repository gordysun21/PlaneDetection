from ultralytics import YOLO

model = YOLO('yolov8n.pt')

#model.train(
#    data='yolo_dataset/dataset.yaml',
#    epochs=1,
#    batch=16,
#    imgsz=640,
#    device='cpu'
#)

model.export(format='onnx')
results = model('yolostuff/test5.jpg')
results[0].show()

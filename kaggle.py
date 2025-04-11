import kagglehub

# Download latest version
path = kagglehub.dataset_download("ahemateja19bec1025/drone-car-counting-dataset-yolo")

print("Path to dataset files:", path)
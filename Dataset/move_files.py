import os

for image in os.listdir("../Dataset/imagenes"):
    if image.endswith(".jpg"):
        print(image)
        name = image.split("_")
        print(name)
        os.rename(f"../Dataset/imagenes/{image}", f"../Dataset/imagenes/{name[0]}_{name[1]}_{name[2]}/{name[0]}_{name[1]}_{name[2]}_{name[3]}")
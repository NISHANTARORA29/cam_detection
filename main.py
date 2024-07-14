import cv2
import os

def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = cv2.imread(os.path.join(folder_path, filename))
            if img is None:
                print(f"Error: Unable to load image {filename}")
            else:
                print(f"Loaded image {filename} successfully. Image shape: {img.shape}")
                images.append(img)
    return images

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges

def stitch_images(images):
    stitcher = cv2.Stitcher.create()
    preprocessed_images = [preprocess_image(img) for img in images]
    status, panorama = stitcher.stitch(preprocessed_images)
    if status == cv2.Stitcher_OK:
        print("Stitching completed successfully.")
        cv2.imwrite('panorama.jpg', panorama)
        cv2.imshow('Panorama', panorama)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"Stitching failed with status {status}")
        if status == cv2.Stitcher_ERR_NEED_MORE_IMGS:
            print("Error: Need more images.")
        elif status == cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL:
            print("Error: Homography estimation failed.")
        elif status == cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL:
            print("Error: Camera parameters adjustment failed.")

if __name__ == "__main__":
    folder_path = './4'  # Change this to the directory containing your images
    images = load_images_from_folder(folder_path)
    if len(images) >= 4:  # Ensure there are at least 4 images
        print("Stitching images...")
        for i, img in enumerate(images):
            print(f"Image {i} shape: {img.shape}")
        stitch_images(images)
    else:
        print(f"Error: Expected at least 4 images, but loaded {len(images)}")

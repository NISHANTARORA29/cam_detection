import cv2

def capture_images():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video device.")
        return []

    directions = ['E', 'W', 'N', 'S']
    images = []

    for direction in directions:
        print(f"Capturing image for {direction} direction. Press 's' to save the image.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                continue
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                images.append(frame)
                print(f"Image for {direction} direction captured.")
                break

    cap.release()
    cv2.destroyAllWindows()
    return images

def stitch_images(images):
    stitcher = cv2.Stitcher.create()
    status, panorama = stitcher.stitch(images)

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
    images = capture_images()
    if images:
        stitch_images(images)

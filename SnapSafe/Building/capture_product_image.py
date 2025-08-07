import cv2
from harmness_detection import Harmness_Detection_function
from harmness_detection import process_barcode_image
def capture_and_crop_image(output_path="captured_product.png"):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Cannot access webcam")
        return

    print("📸 Press SPACE to capture image. Press ESC to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        cv2.imshow("Live Feed - Press SPACE to Capture", frame)
        key = cv2.waitKey(1)
        if key % 256 == 27:  # ESC to exit
            print("👋 Exiting...")
            break
        elif key % 256 == 32:  # SPACE to capture
            img = frame.copy()
            cap.release()
            cv2.destroyAllWindows()

            # Crop using OpenCV ROI selector
            r = cv2.selectROI("Crop Image - Drag to select, ENTER to confirm", img, showCrosshair=True)
            if r == (0, 0, 0, 0):
                print("⚠️ No region selected. Using full image.")
                cropped = img
            else:
                x, y, w, h = r
                cropped = img[y:y+h, x:x+w]

            cv2.imshow("Cropped Image", cropped)
            cv2.imwrite(output_path, cropped)
            print(f"✅ Image saved as: {output_path}", flush=True)
            # cv2.waitKey(0)
            cv2.waitKey(1) 
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("🚀 Starting Product Image Capture...")
    capture_and_crop_image()  # assumes image gets saved as 'captured_product.jpg'

    img_path = "captured_product.jpg"
    print(f"📁 Image saved at: {img_path}")

    # img_path="C:\\Users\\dhruv\\OneDrive\\Documents\\Desktop\\Neural\\Screenshot 2025-06-08 161620.png"
    # img_path="C:\\Users\\dhruv\\OneDrive\\Documents\\Desktop\\Neural\\newwwww.png"
    result = Harmness_Detection_function(img_path)

    # if result:
    #     print("\n🎯 Final Detection Summary:")
    #     print(f"🧪 Chemicals: {result['chemicals']}")
    #     print(f"🧠 Category: {result['category']} | Confidence: {result['confidence']:.2f}")
    #     print(f"📉 Avg Score: {result['average_score']:.2f}%")
    #     print(f"⚠️ Risk Level: {result['risk_level']}")
    #     print(f"📋 Individual Scores: {result['individual_scores']}")

    #     if result['barcode_info']:
    #         print("\n🔍 Barcode Info:")
    #         for item in result['barcode_info']:
    #             print(f"➡️ Title: {item['title']}, Brand: {item['brand']}, Harm Score: {item['harm_score']:.2f}, Risk: {item['risk_level']}")
    #     else:
    #         print("❌ No barcode info available.")
    # else:
    #     print("❌ Detection failed.")



#further advanced will be increased datasets which have more chemicals and it will detect based on weight like 10gm 
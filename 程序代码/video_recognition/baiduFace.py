# 百度人脸情绪检测API
import requests
import json
import cv2
import base64
import time

API_KEY = "OB6MLUL2OugwcYFP5FsoJkPv"
SECRET_KEY = "wtKRkbue4JmWdTQP4z2l437YdV39IBAE"


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        return

    fps = 0
    frame_count = 0
    start_time = time.time()
    last_request_time = time.time() - 3

    while True:
        ret, frame = cap.read()
        frame_count += 1

        if not ret:
            break

        current_time = time.time()
        if current_time - last_request_time >= 3:
            retval, buffer = cv2.imencode('.jpg', frame)
            image = base64.b64encode(buffer).decode('utf-8')

            url = "https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token=" + get_access_token()

            payload = json.dumps({
                "image": image,
                "image_type": "BASE64",
                "face_field": "expression"
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            result = response.json()
            print(result)

            if result['error_code'] == 0:
                # Get the emotion from the response
                if result['result']['face_list']:
                    emotion = result['result']['face_list'][0]['expression']['type']
                    cv2.putText(frame, f'Emotion: {emotion}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                                cv2.LINE_AA)

            last_request_time = current_time

        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time

        cv2.putText(frame, f'FPS: {fps:.2f}', (frame.shape[1] - 100, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    main()

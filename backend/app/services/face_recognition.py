from pathlib import Path

import cv2
import numpy as np

CASCADE_PATH = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
FACE_CASCADE = cv2.CascadeClassifier(str(CASCADE_PATH))


def detect_largest_face_box(image):
    if image is None or image.size == 0:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.08,
        minNeighbors=5,
        minSize=(48, 48),
    )

    if len(faces) == 0:
        return None

    x, y, width, height = max(faces, key=lambda face: face[2] * face[3])
    return int(x), int(y), int(width), int(height)


def crop_face_box(image, face_box, padding_x_ratio=0.15, padding_y_ratio=0.15):
    if image is None or image.size == 0 or face_box is None:
        return None

    x, y, width, height = face_box
    padding_x = int(width * padding_x_ratio)
    padding_y = int(height * padding_y_ratio)
    x0 = max(0, x - padding_x)
    y0 = max(0, y - padding_y)
    x1 = min(image.shape[1], x + width + padding_x)
    y1 = min(image.shape[0], y + height + padding_y)
    return image[y0:y1, x0:x1]


def detect_largest_face(image):
    face_box = detect_largest_face_box(image)
    return crop_face_box(image, face_box)


def face_signature(face_image):
    resized = cv2.resize(face_image, (128, 128))
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [32, 32], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return hist


def signature_similarity(photo_signature, frame_signature):
    score = cv2.compareHist(photo_signature, frame_signature, cv2.HISTCMP_CORREL)
    normalized = int(round(max(0, min(1, (score + 1) / 2)) * 100))
    return normalized


def sample_video_faces(video_path, max_samples=8):
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        return []

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    if frame_count <= 0:
        frame_indexes = range(max_samples)
    else:
        frame_indexes = np.linspace(0, max(0, frame_count - 1), num=max_samples, dtype=int)

    faces = []
    for frame_index in frame_indexes:
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
        ok, frame = capture.read()
        if not ok:
            continue

        face = detect_largest_face(frame)
        if face is not None:
            faces.append(face)

    capture.release()
    return faces


def verify_athlete_face(photo_path, video_path):
    photo_image = cv2.imread(str(photo_path))
    photo_face = detect_largest_face(photo_image)

    if photo_face is None:
        return {
            "status": "photo_face_not_detected",
            "match_confidence": 0,
            "faces_detected_in_video": 0,
            "frames_checked": 0,
            "message": "Nao foi possivel detectar um rosto claro na foto enviada.",
            "method": "opencv_haar_histogram_beta",
        }

    photo_signature = face_signature(photo_face)
    video_faces = sample_video_faces(video_path)

    if not video_faces:
        return {
            "status": "video_face_not_detected",
            "match_confidence": 0,
            "faces_detected_in_video": 0,
            "frames_checked": 8,
            "message": "Nao foi possivel detectar rosto nos frames amostrados do video.",
            "method": "opencv_haar_histogram_beta",
        }

    similarities = [
        signature_similarity(photo_signature, face_signature(face))
        for face in video_faces
    ]
    confidence = max(similarities)

    if confidence >= 74:
        status = "verified"
        message = "Rosto da foto encontrado com boa similaridade nos frames do video."
    elif confidence >= 55:
        status = "review_required"
        message = "Ha indicio de similaridade facial, mas recomenda-se revisao humana."
    else:
        status = "low_confidence"
        message = "A similaridade facial ficou baixa; confirme se a foto e o video sao do mesmo atleta."

    return {
        "status": status,
        "match_confidence": confidence,
        "faces_detected_in_video": len(video_faces),
        "frames_checked": 8,
        "message": message,
        "method": "opencv_haar_histogram_beta",
        "disclaimer": "Verificacao facial beta para apoio operacional; nao substitui validacao humana em casos de baixa qualidade.",
    }

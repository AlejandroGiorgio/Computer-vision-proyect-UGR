import cv2
import numpy as np
import mediapipe as mp
import time
from datetime import datetime

class ExamMonitor:
    def __init__(self, alert_threshold=30, time_threshold=2.0):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Puntos del iris
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]
        
        # Puntos clave del ojo para medir apertura vertical
        # Puntos superiores e inferiores del ojo
        self.LEFT_EYE_TOP = 386     # Punto superior del ojo izquierdo
        self.LEFT_EYE_BOTTOM = 374  # Punto inferior del ojo izquierdo
        self.RIGHT_EYE_TOP = 159    # Punto superior del ojo derecho
        self.RIGHT_EYE_BOTTOM = 145 # Punto inferior del ojo derecho
        
        # Puntos completos del contorno del ojo
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        
        self.alert_threshold = alert_threshold
        self.time_threshold = time_threshold
        self.looking_away_start = None
        self.total_time_looking_away = 0
        self.alerts = []
        self.debug_info = True
        
        # Umbrales para la apertura del ojo
        self.eye_open_threshold = 0.5  # Proporción mínima de apertura del ojo
        
    def calculate_eye_opening(self, top_point, bottom_point, eye_points):
        """
        Calcula la apertura relativa del ojo comparando la distancia actual
        entre los puntos superior e inferior con la altura total del ojo
        """
        eye_height = np.linalg.norm(top_point - bottom_point)
        total_eye_height = np.max(eye_points[:, 1]) - np.min(eye_points[:, 1])
        return eye_height / max(total_eye_height, 1)  # Evitar división por cero

    def get_iris_visibility(self, iris_points, eye_points):
        """
        Calcula qué tan visible está el iris basado en su posición relativa
        y la forma del ojo
        """
        iris_center = np.mean(iris_points, axis=0)
        eye_top = np.min(eye_points[:, 1])
        eye_bottom = np.max(eye_points[:, 1])
        eye_height = eye_bottom - eye_top
        
        # Calcular qué tan cerca está el iris del borde superior o inferior del ojo
        relative_position = (iris_center[1] - eye_top) / max(eye_height, 1)
        
        # Si el iris está muy cerca de los bordes, está parcialmente oculto
        if relative_position < 0.3 or relative_position > 0.6:
            return False
        return True

    def get_iris_position(self, iris_center, eye_points):
        """
        Calcula la posición relativa del iris dentro del ojo
        """
        eye_points = np.array(eye_points)
        
        # Obtener límites del ojo
        left = np.min(eye_points[:, 0])
        right = np.max(eye_points[:, 0])
        top = np.min(eye_points[:, 1])
        bottom = np.max(eye_points[:, 1])
        
        # Calcular posición relativa del iris
        iris_x, iris_y = iris_center
        
        eye_width = max(right - left, 1)
        eye_height = max(bottom - top, 1)
        
        relative_x = (iris_x - left) / eye_width
        relative_y = (iris_y - top) / eye_height
        
        return relative_x, relative_y

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        
        debug_frame = frame.copy()
        
        if not results.multi_face_landmarks:
            if self.debug_info:
                cv2.putText(debug_frame, "No se detecta rostro", (10, 120),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return debug_frame, True, (0, 0)
            
        face_landmarks = results.multi_face_landmarks[0]
        ih, iw, _ = frame.shape
        
        try:
            # Convertir landmarks a coordenadas de píxeles
            mesh_points = np.array([
                np.multiply([p.x, p.y], [iw, ih]).astype(int)
                for p in face_landmarks.landmark
            ])
            
            # Obtener puntos de los ojos y los iris
            left_eye_points = mesh_points[self.LEFT_EYE]
            right_eye_points = mesh_points[self.RIGHT_EYE]
            left_iris_points = mesh_points[self.LEFT_IRIS]
            right_iris_points = mesh_points[self.RIGHT_IRIS]
            
            # Calcular apertura de los ojos
            left_top = mesh_points[self.LEFT_EYE_TOP]
            left_bottom = mesh_points[self.LEFT_EYE_BOTTOM]
            right_top = mesh_points[self.RIGHT_EYE_TOP]
            right_bottom = mesh_points[self.RIGHT_EYE_BOTTOM]
            
            left_opening = self.calculate_eye_opening(left_top, left_bottom, left_eye_points)
            right_opening = self.calculate_eye_opening(right_top, right_bottom, right_eye_points)
            avg_opening = (left_opening + right_opening) / 2
            
            # Verificar visibilidad del iris
            left_iris_visible = self.get_iris_visibility(left_iris_points, left_eye_points)
            right_iris_visible = self.get_iris_visibility(right_iris_points, right_eye_points)
            
            # Obtener posiciones del iris
            left_iris_center = np.mean(left_iris_points, axis=0).astype(int)
            right_iris_center = np.mean(right_iris_points, axis=0).astype(int)
            
            left_x, left_y = self.get_iris_position(left_iris_center, left_eye_points)
            right_x, right_y = self.get_iris_position(right_iris_center, right_eye_points)
            
            # Determinar si está mirando fuera
            looking_away = False
            direction = "PANTALLA"
            
            # Si los ojos están muy cerrados o el iris no es visible la cabeza puede estar perfilada hacia abajo o a los costados
            if avg_opening < self.eye_open_threshold or not (left_iris_visible and right_iris_visible):
                looking_away = True
                direction = "FUERA DE LA PANTALLA"
            else:
                # Verificar posición horizontal del iris sin que la cabeza este perfilada
                avg_x = (left_x + right_x) / 2
                if avg_x < 0.4:
                    looking_away = True
                    direction = "FUERA DE LA PANTALLA (derecha)"
                elif avg_x > 0.6:
                    looking_away = True
                    direction = "FUERA DE LA PANTALLA (izquierda)"

                
            
            # Debug visual
            if self.debug_info:
                # Dibujar contornos de los ojos
                cv2.polylines(debug_frame, [left_eye_points], True, (0, 255, 0), 1)
                cv2.polylines(debug_frame, [right_eye_points], True, (0, 255, 0), 1)
                
                # Dibujar puntos de apertura del ojo
                cv2.circle(debug_frame, left_top, 2, (0, 255, 255), -1)
                cv2.circle(debug_frame, left_bottom, 2, (0, 255, 255), -1)
                cv2.circle(debug_frame, right_top, 2, (0, 255, 255), -1)
                cv2.circle(debug_frame, right_bottom, 2, (0, 255, 255), -1)
                
                # Mostrar información de apertura y visibilidad
                cv2.putText(debug_frame, f"Apertura: {avg_opening:.2f}", (10, 180),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.putText(debug_frame, f"Iris visible: {left_iris_visible and right_iris_visible}", 
                           (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.putText(debug_frame, f"Direccion: {direction}", (10, 240),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Gestionar el tiempo
            current_time = time.time()
            if looking_away:
                if self.looking_away_start is None:
                    self.looking_away_start = current_time
                elif current_time - self.looking_away_start > self.time_threshold:
                    alert_msg = f"Alerta: Mirada desviada ({direction}) por mas de {self.time_threshold} segundos"
                    self.alerts.append((datetime.now(), alert_msg))
                    self.total_time_looking_away += current_time - self.looking_away_start
                    self.looking_away_start = current_time
            else:
                self.looking_away_start = None
            
            # Dibujar información en el frame
            status = f"Mirando: {direction}"
            cv2.putText(debug_frame, status, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                       (0, 0, 255) if looking_away else (0, 255, 0), 2)
            
            cv2.putText(debug_frame, f"Tiempo total fuera: {self.total_time_looking_away:.1f}s", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            if self.total_time_looking_away > self.alert_threshold:
                cv2.putText(debug_frame, f"EXAMEN SUSPENDIDO POR CONDUCTA SOSPECHOSA", 
                       (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            
            return debug_frame, looking_away, (avg_opening, direction)
            
        except Exception as e:
            if self.debug_info:
                cv2.putText(debug_frame, f"Error: {str(e)}", (10, 150),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return debug_frame, True, (0, "ERROR")
    
    def get_alerts(self):
        return self.alerts
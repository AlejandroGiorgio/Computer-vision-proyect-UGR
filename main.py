import cv2
from utils import ExamMonitor
import time

def check_camera():
    """Verifica si la cámara está disponible y funcionando"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False, None
    
    # Intentar leer un frame
    ret, frame = cap.read()
    cap.release()
    
    return ret, frame

def main():
    # Verificar cámara antes de empezar
    camera_ok, test_frame = check_camera()
    if not camera_ok:
        print("Error: No se puede acceder a la cámara web. Por favor, verifique que:")
        print("1. La cámara está conectada")
        print("2. No está siendo usada por otra aplicación")
        print("3. Tiene los permisos necesarios para acceder a la cámara")
        return

    # Inicializar la captura de video con configuración específica
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Usar CAP_DSHOW en Windows
    
    # Configurar parámetros de la cámara
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    if not cap.isOpened():
        print("Error: No se pudo inicializar la cámara.")
        return
    
    monitor = ExamMonitor(alert_threshold=20)                          #Customizar los thresholds tanto de las alertas como la tolerancia de suspension de examen
    print("Iniciando monitoreo... Presione 'q' para salir.")
    
    # Dar tiempo a la cámara para inicializarse
    time.sleep(2)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: No se pudo leer el frame de la cámara.")
                break
                
            # Procesar frame
            try:
                processed_frame, looking_away, angle = monitor.process_frame(frame)
                
                # Mostrar resultado
                cv2.imshow('Exam Monitor', processed_frame)
                
                # Salir con 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\nDetección finalizada por el usuario.")
                    break
                    
            except Exception as e:
                print(f"Error procesando frame: {e}")
                continue
                
    except KeyboardInterrupt:
        print("\nDetección interrumpida por el usuario.")
    
    finally:
        # Limpiar
        cap.release()
        cv2.destroyAllWindows()
        
        # Imprimir resumen de alertas
        print("\nResumen de alertas:")
        for timestamp, alert in monitor.get_alerts():
            print(f"{timestamp}: {alert}")

if __name__ == "__main__":
    main()
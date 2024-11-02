Sistema de Detección de Trampas en Exámenes Virtuales
Este proyecto implementa un sistema de monitoreo en tiempo real que utiliza visión por computadora para detectar cuando un estudiante desvía su mirada de la pantalla durante un examen virtual, ayudando a mantener la integridad académica en entornos de evaluación remota.
Características

👁 Detección y seguimiento facial en tiempo real
📊 Cálculo de la dirección de la mirada
⏱ Monitoreo del tiempo de desvío de la mirada
🚨 Sistema de alertas automáticas
📝 Registro de eventos y generación de informes

Requisitos Previos

Python 3.8 - 3.10 (recomendado: 3.10)
Cámara web funcional
Sistema operativo: Windows 10/11, macOS, o Linux

Instalación

Clone el repositorio:

bashCopygit clone https://github.com/yourusername/exam-monitoring-system.git
cd exam-monitoring-system

Cree un entorno virtual:

bashCopy# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate

Instale las dependencias:

bashCopypip install -r requirements.txt
Uso

Active el entorno virtual (si no está activado):

bashCopy# Windows
.\venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

Ejecute el programa:

bashCopypython exam_monitor.py

Controles:


Presione 'q' para salir del programa
Las alertas se mostrarán en la pantalla cuando se detecte un desvío prolongado de la mirada
Al finalizar, se generará un resumen de todas las alertas registradas

Configuración
Puede modificar los siguientes parámetros en la clase ExamMonitor:

alert_threshold: Ángulo máximo permitido de desviación (por defecto: 30 grados)
time_threshold: Tiempo máximo permitido mirando fuera (por defecto: 2.0 segundos)

Estructura del Proyecto
Copyexam-monitoring-system/
│
├── exam_monitor.py       # Archivo principal del programa
├── requirements.txt      # Dependencias del proyecto
├── README.md            # Este archivo
└── venv/                # Entorno virtual (generado durante la instalación)
Limitaciones Conocidas

Requiere buena iluminación para una detección óptima
La precisión puede variar según la calidad de la cámara
No funciona con gafas de sol o elementos que obstaculicen la vista de los ojos

Contribuir

Fork el proyecto
Cree una nueva rama (git checkout -b feature/nueva-caracteristica)
Commit sus cambios (git commit -am 'Añade nueva característica')
Push a la rama (git push origin feature/nueva-caracteristica)
Abra un Pull Request

Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
Autor

Alejandro Giorgio

Agradecimientos

MediaPipe por su excelente framework de visión por computadora
OpenCV por sus herramientas de procesamiento de imágenes
La comunidad de Python por sus contribuciones
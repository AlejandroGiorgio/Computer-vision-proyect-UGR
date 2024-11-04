# Sistema de Detección de Trampas en Exámenes Virtuales
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

Clonar el repositorio:
clone https://github.com/AlejandroGiorgio/Computer-vision-proyect-UGR.git

Cree un entorno virtual:

# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate

## Instale las dependencias:

install -r requirements.txt

## Uso

Active el entorno virtual (si no está activado):

# Windows
.\venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

## Ejecute el programa:

python main.py

Controles:

Presione 'q' para salir del programa. 

Las alertas se mostrarán en la pantalla cuando se detecte un desvío prolongado de la mirada. 

Al finalizar, se generará un resumen de todas las alertas registradas. 

Configuración: 

Puede modificar los siguientes parámetros en la clase ExamMonitor:

alert_threshold: tiempo máximo permitido de desviación antes de suspender el examen (por defecto: 30 segundos)

time_threshold: Tiempo máximo permitido mirando fuera antes de generar una alerta (por defecto: 2.0 segundos)

Estructura del Proyecto
Copyexam-monitoring-system/
│
├── utils.py       # Funciones auxiliares y clase que maneja la deteccion de rostros
├── main.py        # Archivo donde se corre el programa y se puede customizar tanto el time_threshold asi como el alert_thershold
├── requirements.txt      # Dependencias del proyecto
├── README.md            # Este archivo
└── venv/                # Entorno virtual (generado durante la instalación)
Limitaciones Conocidas

Requiere buena iluminación para una detección óptima
La precisión puede variar según la calidad de la cámara
No funciona con gafas de sol o elementos que obstaculicen la vista de los ojos

Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
Autor

Alejandro Giorgio
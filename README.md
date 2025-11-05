# 🩺 Mortalidad en Colombia 2019 - Dashboard Interactivo

## 📘 Introducción del proyecto
Este proyecto desarrolla una aplicación web dinámica en **Python** utilizando **Plotly Dash**, que permite analizar los datos de mortalidad en Colombia durante el año 2019.  
La aplicación fue diseñada con fines académicos para mostrar cómo los datos pueden transformarse en visualizaciones interactivas que faciliten la comprensión de patrones, tendencias y diferencias demográficas a nivel nacional.

---

## 🎯 Objetivo
El objetivo principal de la aplicación es **analizar la distribución de la mortalidad en Colombia en 2019**, identificando patrones relacionados con:
- Diferencias regionales por departamento.
- Variaciones mensuales de las muertes.
- Principales causas de defunción.
- Distribución por sexo y grupo etario.

La herramienta busca apoyar la interpretación visual de los datos, fortaleciendo habilidades en **análisis de datos, visualización y despliegue en la nube**.

---

## 🧩 Estructura del proyecto

├── app.py # Código principal de la aplicación Dash
├── requirements.txt # Librerías necesarias para ejecutar la app
├── Procfile # Archivo para definir el comando de ejecución en Render
├── runtime.txt # Versión de Python utilizada en el despliegue
├── README.md # Documentación del proyecto
│
└── data/ # Carpeta que contiene los archivos de entrada


---

## ⚙️ Requisitos

| Librería | Versión recomendada |
|-----------|--------------------|
| dash | 2.17.1 |
| plotly | 5.24.1 |
| pandas | 2.3.0 |
| openpyxl | 3.1.5 |
| gunicorn | 21.2.0 |

> Todas las dependencias se instalan automáticamente desde el archivo `requirements.txt`.

---

## Instalación local

1. Clona este repositorio:  https://github.com/FrankOrtegon/dashboard-colombia-mortalidad-2019.git
2. Crea un entorno virtual y actívalo:
python -m venv .venv
.venv\Scripts\activate

3. Instala las dependencias: pip install -r requirements.txt
4. Ejecuta la aplicación: python app.py
5. Abre tu navegador y accede a: http://127.0.0.1:8050


---

## Visualizaciones y hallazgos principales

1. Distribución total de muertes por departamento

Representa la cantidad total de muertes en cada departamento colombiano durante 2019.
Los círculos de mayor tamaño indican departamentos con más fallecimientos, como Antioquia, Valle del Cauca y Cundinamarca, reflejando la relación con la densidad poblacional.

2. Muertes por mes

Gráfico de líneas que muestra el comportamiento mensual de las defunciones.
Se observan picos durante los meses de junio y diciembre, posiblemente relacionados con eventos climáticos o festividades.

3. Ciudades más violentas (código X95)

Barras que representan las 5 ciudades con mayor número de muertes por agresión con arma de fuego.
Las ciudades más afectadas suelen concentrarse en zonas urbanas de alta densidad y conflicto.

4. Ciudades con menor mortalidad

Gráfico circular que destaca las 10 ciudades con menor índice de mortalidad total.
Estas zonas suelen ser municipios pequeños o rurales con menor concentración poblacional.

5. Principales causas de muerte

Tabla que lista las 10 causas más frecuentes de defunción en Colombia, ordenadas de mayor a menor ocurrencia, con su respectivo código CIE10.

6. Muertes por sexo y departamento

Gráfico de barras apiladas que permite comparar visualmente las diferencias de mortalidad entre hombres y mujeres por departamento.
En la mayoría de regiones, el número de muertes masculinas supera al de las femeninas.

7. Distribución por grupo de edad

Histograma que clasifica las muertes según el grupo etario (GRUPO_EDAD1) definido por el DANE.
Se observa una mayor concentración de defunciones en la adultez intermedia y la vejez, lo que es consistente con las etapas de mayor vulnerabilidad biológica.

---

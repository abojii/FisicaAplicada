# ⚡ Proyecto: Ley de Coulomb - Principio de Superposición

Aplicación web interactiva desarrollada con **Streamlit** para calcular, visualizar y explicar la **fuerza eléctrica neta** que actúa sobre una carga objetivo, aplicando la **Ley de Coulomb** y el **Principio de Superposición**.

---

## 🧠 Descripción

Esta aplicación permite ingresar una carga objetivo y múltiples cargas puntuales en el plano cartesiano. A partir de estos datos, el sistema:

- Calcula la fuerza eléctrica que ejerce cada carga sobre la carga objetivo
- Descompone cada fuerza en sus componentes en X y Y
- Suma todas las fuerzas mediante el principio de superposición
- Obtiene la fuerza neta total (vectorial)
- Calcula la magnitud del vector resultante
- Muestra una representación gráfica del sistema
- Explica paso a paso el procedimiento matemático

---

## 📐 Fundamento teórico

### Ley de Coulomb

La fuerza entre dos cargas puntuales se define como:

\[
F = k \frac{q_1 q_2}{r^2}
\]

Donde:

- \( F \): fuerza eléctrica
- \( k \): constante de Coulomb (\(9 \times 10^9\))
- \( q_1, q_2 \): cargas
- \( r \): distancia entre ellas

### Forma vectorial

\[
F_x = k \frac{q_0 q_i \, dx}{r^3}
\]
\[
F_y = k \frac{q_0 q_i \, dy}{r^3}
\]

---

## 🔢 Funcionalidades

- Entrada flexible de datos (notación científica: `2x10^-6`, `2e-6`, etc.)
- Ingreso de posiciones en formato `(x,y)`
- Cálculo automático de fuerzas individuales
- Suma vectorial (superposición)
- Visualización gráfica tipo plano cartesiano
- Vector de fuerza neta dinámico
- Procedimiento paso a paso explicado
- Interfaz moderna estilo aplicación web

---

## 📊 Ejemplo de uso

### Entrada:

- Carga objetivo:
  - \( q_0 = 2 \times 10^{-6} \)
  - Posición: (0,0)

- Cargas:
  - \( q_1 = 3 \times 10^{-6} \) en (1,0)
  - \( q_2 = -4 \times 10^{-6} \) en (0,1)

### Resultado esperado:

- Fuerza hacia arriba e izquierda
- Vector neto diagonal
- Magnitud calculada automáticamente

---

## 🚀 Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/proyecto-coulomb.git
cd proyecto-coulomb

# Configuración del entorno
1. Crear entorno virtual
```console
    python3 -m venv .venv
```
2. Instalar dependencias
```console
    pip install numpy scikit-learn pandas
```
# Manual de ejecución
* Formato:
```console
    Usage: python MineSweeper.py width height mines player [--record-data] <player arguments>
```
* Ejemplo:
```console
    python MineSweeper.py 8 8 10 Player/LogisticRegressionBot.py
```
## Pruebas
* Formato: 
```console
    Usage: python3 BotBenchMark.py number_tests
```
* Ejemplo: El precargado con el repositorio tiene 400 pruebas
```console
    Usage: python BotBenchMark.py 10
```
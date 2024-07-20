# Ddosia-targets

Esta carpeta contiene una guía para extraer los objetivos del grupo NoName057(16) directamente desde la memoria utilizando técnicas básicas de ingeniería inversa con Frida.

Los scripts estan en:
https://github.com/M3str3/ddosia-targets/tree/main

## Pasos para extraer los objetivos

1. **Obtener un client_id**: Registrarse con el BOT del grupo para obtener el `client_id.txt`.
2. **Acceder al canal**: Obtener acceso al canal donde comparten el cliente y la IP del servidor C2.
3. **Preparar el entorno**:
    - Crear una carpeta con el cliente DDoSia para Windows, el `client_id.txt` y una subcarpeta llamada `dumps`.
    - Instalar Frida:
      ```sh
      python -m pip install frida-tools
      ```
4. **Ejecutar el cliente con Frida**:
    ```sh
    frida.exe -l targets.js ./d_win_x64.exe -- -p http://IPNONAME
    ```
5. **Ejecutar el script de Python para recuperar los objetivos**:
    ```sh
    python recover.py --out
    ```

## Mas

Para leer: https://m3str3.vercel.app/posts/ddosia-targets-from-memory
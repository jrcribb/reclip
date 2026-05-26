import os
import argparse
import subprocess
import sys

try:
    import pyperclip
except ImportError:
    pyperclip = None

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")

def download(url, format_choice):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    print(f"\nDescargando {url} en formato {format_choice.upper()}...")
    
    out_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    
    cmd = ["yt-dlp", "--no-playlist", "-o", out_template]
    
    if format_choice == "mp3":
        cmd += ["-x", "--audio-format", "mp3"]
    else:
        cmd += ["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", "--merge-output-format", "mp4"]
        
    cmd.append(url)
    
    try:
        # Usamos subprocess.run para que la salida de yt-dlp se muestre directamente en la consola
        subprocess.run(cmd, check=True)
        print("\n¡Descarga completada con éxito!")
        print(f"Los archivos se han guardado en: {DOWNLOAD_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"\nError durante la descarga: El comando yt-dlp falló (código de salida {e.returncode})")
    except FileNotFoundError:
        print("\nError: No se encontró 'yt-dlp'. Asegúrate de que esté instalado y en el PATH.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")

def interactive_mode():
    print("=== ReClip - Descargador de Consola ===")
    url = ""
    
    # Intentar obtener del portapapeles
    if pyperclip:
        try:
            clipboard_content = pyperclip.paste().strip()
            if clipboard_content.startswith("http://") or clipboard_content.startswith("https://"):
                use_clipboard = input(f"Se detectó una URL en el portapapeles:\n{clipboard_content}\n¿Deseas usar esta URL? (s/n): ").strip().lower()
                if use_clipboard in ['s', 'si', 'y', 'yes']:
                    url = clipboard_content
        except Exception:
            pass
    else:
        print("Nota: La librería 'pyperclip' no está instalada. Para pegar desde el portapapeles automáticamente, instálala usando: pip install pyperclip")

    if not url:
        url = input("Por favor, pega o escribe la URL del video: ").strip()
        
    if not url:
        print("No se proporcionó ninguna URL. Saliendo.")
        return

    print("\nSelecciona el formato de descarga:")
    print("1. MP4 (Video)")
    print("2. MP3 (Audio)")
    
    while True:
        choice = input("Ingresa tu opción (1 o 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Opción inválida. Por favor ingresa 1 o 2.")
    
    format_choice = "mp3" if choice == '2' else "mp4"
        
    download(url, format_choice)

def main():
    parser = argparse.ArgumentParser(description="ReClip - Descargador por línea de comandos usando yt-dlp")
    parser.add_argument("url", nargs="?", help="URL del video a descargar")
    parser.add_argument("-f", "--format", choices=["mp4", "mp3"], help="Formato de descarga (mp4 o mp3)")
    
    args = parser.parse_args()
    
    if args.url:
        format_choice = args.format if args.format else "mp4"
        download(args.url, format_choice)
    else:
        # Si no se pasan argumentos, entrar en modo interactivo
        interactive_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario. Saliendo.")
        sys.exit(0)

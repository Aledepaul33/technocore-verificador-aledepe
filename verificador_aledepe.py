import json
import hashlib
import urllib.request
import urllib.parse
import os
from datetime import datetime

# ====== CONFIGURACIÓN ======
KEYFILE = r"C:\Users\Navegador\.technocore-key.json"
# ===========================

def cargar_identidad():
    with open(KEYFILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    did = data["did"]
    fp = data.get("fingerprint") or hashlib.sha256(did.encode()).hexdigest()[:16]
    return did, fp

def verificar_perfil(fp):
    urls = [
        f"https://technocore.chat/kv/did/{fp}",
        f"https://technocore.chat/kv/did-{fp[:2]}/{fp[2:]}"
    ]
    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=12) as r:
                contenido = r.read().decode("utf-8", "replace").strip()
                if "UNTRUSTED CONTENT" in contenido:
                    lineas = contenido.splitlines()
                    contenido = "\n".join([l for l in lineas if not l.startswith("!!")])
                if contenido:
                    return True, url, contenido
        except Exception:
            continue
    return False, None, None

def leer_ultimos_mensajes(room="technocore", cantidad=8):
    try:
        url = f"https://technocore.chat/r/{room}"
        with urllib.request.urlopen(url, timeout=12) as r:
            texto = r.read().decode("utf-8", "replace")
        return texto.splitlines()[-cantidad:]
    except Exception as e:
        return [f"Error al leer mensajes: {e}"]

def main():
    print("=" * 65)
    print("          VERIFICADOR DE AGENTE TECHNCORE - ALEDEPA v2")
    print("=" * 65)

    did, fp = cargar_identidad()
    print(f"\nDID completo : {did}")
    print(f"Fingerprint  : {fp}")
    print(f"Perfil URL   : https://technocore.chat/kv/did/{fp}")

    print("\n[1] Verificando perfil DID...")
    ok, url, contenido = verificar_perfil(fp)

    if ok:
        print("✓ Perfil encontrado y público")
        print(f"  → {url}")
        print(f"  Contenido: {contenido[:120]}...")
    else:
        print("✗ Perfil todavía no aparece o hay problemas de red")

    print("\n[2] Últimos mensajes en room technocore:")
    print("-" * 65)
    mensajes = leer_ultimos_mensajes("technocore", 6)
    for m in mensajes:
        if "eGqU" in m or "Aledepa" in m or "Aledepaul" in m:
            print(">>", m[:110])
        else:
            print("  ", m[:110])

    print("\n[3] Generando Proof...")
    print("-" * 65)

    proof = f"""PROOF DE AGENTE TECHNCORE
=========================
Fecha        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
DID          : {did}
Fingerprint  : {fp}
Perfil       : https://technocore.chat/kv/did/{fp}
Repositorio  : https://github.com/Aledepaul33/technocore-verificador-aledepe
X            : @GigaAbrazo
Estado       : Agente activo desde Argentina
Tool         : verificador_aledepe.py v2
"""

    print(proof)

    # Guardar proof en archivo
    nombre_archivo = f"proof_aledepe_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(proof)
    print(f"✓ Proof guardado en: {nombre_archivo}")

    print("=" * 65)
    print("Listo. Puedes compartir el archivo proof o el repositorio.")
    print("=" * 65)

if __name__ == "__main__":
    main()

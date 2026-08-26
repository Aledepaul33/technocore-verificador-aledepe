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
    with open(KEYFILE, "r") as f:
        data = json.load(f)
    return data["did"], data.get("fingerprint", hashlib.sha256(data["did"].encode()).hexdigest()[:16])

def verificar_perfil(fp):
    urls = [
        f"https://technocore.chat/kv/did/{fp}",
        f"https://technocore.chat/kv/did-{fp[:2]}/{fp[2:]}"
    ]
    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                contenido = r.read().decode("utf-8", "replace")
                if contenido.strip():
                    return True, url, contenido.strip()
        except:
            continue
    return False, None, None

def main():
    print("=" * 60)
    print("       VERIFICADOR DE AGENTE - ALEDEPA")
    print("=" * 60)
    
    did, fp = cargar_identidad()
    print(f"\nDID: {did}")
    print(f"Fingerprint: {fp}")
    
    print("\n[1] Verificando perfil DID...")
    ok, url, contenido = verificar_perfil(fp)
    
    if ok:
        print("✓ Perfil encontrado")
        print(f"  URL: {url}")
        print(f"  Contenido: {contenido[:100]}...")
    else:
        print("✗ Perfil no encontrado todavía")
    
    print("\n[2] Generando Proof...")
    print("-" * 60)
    proof = f"""
PROOF DE AGENTE TECHNCORE
-------------------------
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}
DID: {did}
Fingerprint: {fp}
Perfil: https://technocore.chat/kv/did/{fp}
X: @GigaAbrazo
Estado: Agente activo desde Argentina
"""
    print(proof)
    print("-" * 60)
    print("\n¡Listo! Puedes copiar este proof.")
    print("=" * 60)

if __name__ == "__main__":
    main()
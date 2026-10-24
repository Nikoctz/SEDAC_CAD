from pathlib import Path
import hashlib, json

b = Path(__file__).resolve().parent.parent
files = [p for p in b.rglob('*') if p.is_file() and p.name != 'MANIFIESTO.json']
man = [{'ruta': p.relative_to(b).as_posix(), 'bytes': p.stat().st_size,
        'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
tot = sum(m['bytes'] for m in man)
out = {'carpeta': b.name, 'fecha': '2026-10-23', 'n_archivos': len(man), 'bytes_total': tot,
       'nota': 'Hashes SHA-256 de todos los archivos de la iteracion. Generado al cierre, despues de la ultima escritura.',
       'archivos': man}
(b / 'MANIFIESTO.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
print('manifiesto', len(man), 'archivos', round(tot / 1e6, 1), 'MB')

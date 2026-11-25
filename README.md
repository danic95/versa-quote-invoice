# VERSA Quote & Invoice · Cotización y Factura

Plantillas de cotización y factura de VERSA Technologies LLC, en inglés y español. Funcionan 100% en el navegador: no hay backend ni base de datos.

**Usar:** https://danic95.github.io/versa-quote-invoice/

| Versión | Ruta | Numeración por defecto |
|---|---|---|
| English | `/en/` | `Q-0001`, `INV-0001` |
| Español | `/es/` | `COT-0001`, `FAC-0001` |

## Cómo funciona
- **Borrador:** se guarda solo en `localStorage` del navegador que uses. Cada idioma tiene su propio borrador y numeración. Otro navegador o computadora empieza de cero.
- **Imprimir o guardar PDF:** abre el documento limpio en una pestaña nueva con el diálogo de impresión. Elige *Guardar como PDF*. Si no abre, permite ventanas emergentes para el sitio.
- **Descargar archivo:** baja un `.html` autocontenido que puedes archivar o reimprimir después.
- El número siguiente sube al imprimir o descargar un documento con el número actual.
- Montos en centavos enteros (BigInt). Cada línea se redondea al centavo y el impuesto se aplica al subtotal.

## Editar la plantilla
La fuente es `tools/template-source.html` (versión en inglés). Las páginas `en/` y `es/` se generan con:

```bash
python3 tools/build.py
```

Los textos en español están en `tools/build.py`. Si cambias un texto de la fuente que tiene traducción, el script falla y te dice cuál: actualiza la línea correspondiente.

## Privacidad
El repo es público, pero no contiene datos de clientes. Lo que llenas se queda en tu navegador. Las páginas llevan `noindex` para no aparecer en buscadores.

"""Genera en/index.html y es/index.html desde tools/template-source.html.
Uso: python3 tools/build.py
"""
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=open(os.path.join(HERE,'template-source.html'),encoding='utf-8').read()
OUT=os.path.dirname(HERE)

class Doc:
    def __init__(s,t): s.t=t
    def rep(s,old,new,n=1):
        c=s.t.count(old)
        assert c==n,(old[:90],c,n)
        s.t=s.t.replace(old,new)

def common(lang,L,title,desc,other):
    body=SRC.split('<body>\n',1)[1]
    skel_style=SRC.split('<style>',1)[1].split('</style>',1)[0]
    d=Doc(body)
    d.rep('<title>Quote & Invoice Template</title>\n','')
    d.rep('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;700&display=swap">\n','')
    d.rep('var KEY="versa.quote-invoice.v2";','var KEY="versa.quote-invoice.'+lang+'.v1";')
    d.rep('function slug(s){return String(s||"").toLowerCase()','function slug(s){return String(s||"").normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase()')
    d.rep('.btn.small{','a.btn{text-decoration:none}\n@media (max-width:699px){.bar{position:static}}\n.btn.small{')
    d.rep('<button type="button" class="btn" id="btnNew">New document</button>\n      <button type="button" class="btn primary" id="btnDl">Download for printing</button>',
          '<a class="btn" href="'+other['href']+'" hreflang="'+other['lang']+'" lang="'+other['lang']+'">'+other['label']+'</a>\n      <button type="button" class="btn" id="btnNew">New document</button>\n      <button type="button" class="btn" id="btnDl">Download file</button>\n      <button type="button" class="btn primary" id="btnPrint">Print or save PDF</button>')
    a=d.t.index('async function download(){'); b=d.t.index('/* ---------- events ---------- */')
    d.t=d.t[:a]+'''var L='''+L+''';
function bumpNumber(num){var nk=state.type==="quote"?"nextQ":"nextI";if(num===numberFor(state.type)){setF(nk,String((parseInt(fv(nk),10)||1)+1));scheduleSave();return true}return false}
function fileName(){return(slug(fv("number"))||state.type)+(fv("custName")?"-"+slug(fv("custName")):"")+".html"}
function saveBlob(name,html){var b=new Blob([html],{type:"text/html"});var u=URL.createObjectURL(b);var a=document.createElement("a");a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},4000)}
function savedMsg(name,bumped){return L.saved(name)+(bumped?" "+L.next(numberFor(state.type)):"")+" "+L.printHint}
async function download(){
  var num=fv("number"),html=buildExport(),name=fileName();
  var dl=null;try{dl=window.claude&&window.claude.use?await window.claude.use("downloads"):null}catch(e){}
  if(!dl){try{saveBlob(name,html);toast(savedMsg(name,bumpNumber(num)))}catch(e){toast(L.cantSave)}return}
  try{var r=await dl.save({filename:name,data:html});if(r&&r.status==="saved")toast(savedMsg(name,bumpNumber(num)))}
  catch(e){if(e&&e.code==="declined")return;toast(e&&e.code==="rate_limited"?L.rate:L.cantSave)}
}
function printDoc(){
  var num=fv("number");
  var html=buildExport().replace("</body>","<script>window.addEventListener('load',function(){setTimeout(function(){window.print()},400)})<\\/script></body>");
  var w=null;try{w=window.open("","_blank")}catch(e){}
  if(!w){toast(L.popup);return}
  w.document.open();w.document.write(html);w.document.close();
  toast(bumpNumber(num)?L.printOpened+" "+L.next(numberFor(state.type)):L.printOpened);
}

'''+d.t[b:]
    d.rep('$("#btnDl").addEventListener("click",download);','$("#btnDl").addEventListener("click",download);\n$("#btnPrint").addEventListener("click",printDoc);\nwindow.addEventListener("pagehide",function(){if(saveTimer){clearTimeout(saveTimer);save()}});')
    head=('<!doctype html>\n<html lang="'+lang+'">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
          '<title>'+title+'</title>\n<meta name="description" content="'+desc+'">\n<meta name="robots" content="noindex">\n'
          '<link rel="icon" href="../favicon.svg" type="image/svg+xml">\n'
          '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
          '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;700&display=swap">\n'
          '<style>'+skel_style+'</style>\n</head>\n<body>\n')
    return head, d

L_EN='''{saved:function(n){return "Saved "+n+"."},next:function(x){return "Next number: "+x+"."},printHint:"Open the file and print it to get a PDF.",cantSave:"The file could not be saved here.",rate:"A save prompt is already open. Answer it, then try again.",popup:"Your browser blocked the print window. Allow pop-ups for this site and try again.",printOpened:"Print window opened. Choose Save as PDF to get a PDF."}'''
L_ES='''{saved:function(n){return "Se guardó "+n+"."},next:function(x){return "Siguiente número: "+x+"."},printHint:"Abre el archivo e imprímelo para obtener el PDF.",cantSave:"No se pudo guardar el archivo aquí.",rate:"Ya hay una ventana de guardado abierta. Respóndela y vuelve a intentar.",popup:"Tu navegador bloqueó la ventana de impresión. Permite ventanas emergentes para este sitio y vuelve a intentar.",printOpened:"Se abrió la ventana de impresión. Elige Guardar como PDF para obtener el PDF."}'''

# ---------- EN ----------
head,d=common('en',L_EN,'VERSA Quote and Invoice','Fill in VERSA Technologies quotes and invoices and print them to PDF.',{'href':'../es/','lang':'es','label':'Español'})
d.rep('price:"2400"},','price:"2,400.00"},');d.rep('price:"95"},','price:"95.00"},');d.rep('price:"1800"}];','price:"1,800.00"}];')
d.rep('o.cName="VERSA Technologies";','o.cName="VERSA Technologies LLC";')
os.makedirs(OUT+'/en',exist_ok=True)
open(OUT+'/en/index.html','w',encoding='utf-8').write(head+d.t+'</body>\n</html>\n')

# ---------- ES ----------
head,d=common('es',L_ES,'VERSA Cotización y Factura','Llena cotizaciones y facturas de VERSA Technologies e imprímelas en PDF.',{'href':'../en/','lang':'en','label':'English'})
R=d.rep
# chrome
R('<h1>Quote &amp; invoice template</h1>','<h1>Plantilla de cotización y factura</h1>')
R('id="saveNote">Fill it in, then download the file to print or send.<','id="saveNote">Llénala y luego imprímela o descarga el archivo para enviarla.<')
R('aria-label="Document type"','aria-label="Tipo de documento"')
R('id="tabQ" aria-pressed="true">Quote<','id="tabQ" aria-pressed="true">Cotización<')
R('id="tabI" aria-pressed="false">Invoice<','id="tabI" aria-pressed="false">Factura<')
R('id="btnNew">New document<','id="btnNew">Nuevo documento<')
R('id="btnDl">Download file<','id="btnDl">Descargar archivo<')
R('id="btnPrint">Print or save PDF<','id="btnPrint">Imprimir o guardar PDF<')
R('<span>This is sample data so you can see how the totals work. Your company details and numbering stay when you start blank.</span>','<span>Estos son datos de ejemplo para que veas cómo funcionan los totales. Los datos de tu empresa y la numeración se conservan al empezar en blanco.</span>')
R('id="btnBlank">Start blank<','id="btnBlank">Empezar en blanco<')
R('aria-label="Document">','aria-label="Documento">')
R('<aside class="side" aria-label="Defaults">','<aside class="side" aria-label="Valores predeterminados">')
R('<h2 id="defT">Defaults</h2>','<h2 id="defT">Predeterminados</h2>')
R('<p class="cap">Used every time you start a new document.</p>','<p class="cap">Se usan cada vez que empiezas un documento nuevo.</p>')
R('for="defTax">Tax rate, %<','for="defTax">Impuesto, %<')
R('for="defNet">Invoice terms<','for="defNet">Plazo de factura<')
R('for="prefixQ">Quote prefix<','for="prefixQ">Prefijo de cotización<')
R('for="nextQ">Next quote no.<','for="nextQ">Siguiente n.º cotización<')
R('for="prefixI">Invoice prefix<','for="prefixI">Prefijo de factura<')
R('for="nextI">Next invoice no.<','for="nextI">Siguiente n.º factura<')
R('<p class="note">Each line is rounded to the cent, then tax is applied to the subtotal and rounded half up. The next number goes up after you download a document with the current number.</p>','<p class="note">Cada línea se redondea al centavo; luego el impuesto se aplica al subtotal y se redondea al centavo más cercano. El número siguiente sube cuando descargas o imprimes un documento con el número actual.</p>')
# paper
R('alt="Company logo"','alt="Logo de la empresa"')
R('for="logoFile">Change logo<','for="logoFile">Cambiar logo<')
R('id="logoReset">Use VERSA logo<','id="logoReset">Usar logo de VERSA<')
R('data-q="Quote" data-i="Invoice">Quote</h2>','data-q="Cotización" data-i="Factura">Cotización</h2>')
R('for="number">Number<','for="number">Número<')
R('for="status">Status<','for="status">Estado<')
R('<h3>From</h3>','<h3>De</h3>'); R('<h3>Bill to</h3>','<h3>Para</h3>')
R('for="cName">Company<','for="cName">Empresa<'); R('placeholder="Your company name"','placeholder="Nombre de tu empresa"')
R('for="cAddress">Address<','for="cAddress">Dirección<'); R('for="custAddress">Billing address<','for="custAddress">Dirección<')
R('placeholder="Street, city, state ZIP"','placeholder="Calle, ciudad, estado, código postal"',2)
R('for="cEmail">Email<','for="cEmail">Correo<'); R('for="custEmail">Email<','for="custEmail">Correo<')
R('placeholder="office@yourcompany.com"','placeholder="oficina@tuempresa.com"')
R('for="cPhone">Phone<','for="cPhone">Teléfono<'); R('for="custPhone">Phone<','for="custPhone">Teléfono<')
R('for="custName">Customer<','for="custName">Cliente<'); R('placeholder="Customer or company name"','placeholder="Nombre del cliente o empresa"')
R('for="issued">Issue date<','for="issued">Fecha de emisión<')
R('data-q="Quote valid for" data-i="Payment terms">Payment terms<','data-q="Cotización válida por" data-i="Condiciones de pago">Condiciones de pago<')
R('data-q="Valid until" data-i="Due date">Due date<','data-q="Válida hasta" data-i="Fecha de vencimiento">Fecha de vencimiento<')
R('for="reference">PO or reference<','for="reference">Orden de compra o referencia<'); R('placeholder="Optional"','placeholder="Opcional"')
R('for="projName">Project<','for="projName">Proyecto<'); R('placeholder="Project or engagement name"','placeholder="Nombre del proyecto"')
R('data-q="Scope of work" data-i="Work covered">Scope of work<','data-q="Alcance del trabajo" data-i="Trabajo cubierto">Alcance del trabajo<')
R('aria-label="Scope of work" placeholder="Describe what is included, and what is not."','aria-label="Alcance del trabajo" placeholder="Describe qué incluye y qué no."')
R('<span>Description</span><span class="r">Qty</span><span>Unit</span><span class="r">Unit price</span><span class="r">Amount</span>','<span>Descripción</span><span class="r">Cant.</span><span>Unidad</span><span class="r">Precio unit.</span><span class="r">Importe</span>')
R('id="addLine">Add line<','id="addLine">Agregar línea<')
R('<option value="ea"><option value="hr"><option value="day"><option value="mo"><option value="ls">','<option value="u"><option value="h"><option value="día"><option value="mes"><option value="gl">')
R('<span>Tax <span class="rate">','<span>Impuesto <span class="rate">'); R('aria-label="Tax rate in percent"','aria-label="Tasa de impuesto en porcentaje"')
R('<h3>How to pay</h3>','<h3>Cómo pagar</h3>')
R('aria-label="How to pay" placeholder="Who to make checks out to, and bank transfer or Zelle details."','aria-label="Cómo pagar" placeholder="A nombre de quién van los cheques y datos de transferencia o Zelle."')
R('<h3>Terms</h3>','<h3>Términos</h3>'); R('aria-label="Terms"','aria-label="Términos"')
R('<div>Accepted by (signature)</div><div>Date</div>','<div>Aceptado por (firma)</div><div>Fecha</div>')
R('aria-label="Closing line" placeholder="Closing line"','aria-label="Línea de cierre" placeholder="Línea de cierre"')
# JS
R('var MONTHS=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];','var MONTHS=["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];')
R('return MONTHS[p[1]-1]+" "+p[2]+", "+p[0]}','return p[2]+" "+MONTHS[p[1]-1]+" "+p[0]}')
R('var STATUS={quote:["Pending","Accepted","Declined"],invoice:["Draft","Sent","Paid","Void"]};','var STATUS={quote:["Pendiente","Aceptada","Rechazada"],invoice:["Borrador","Enviada","Pagada","Anulada"]};')
R('quote:[["7","Valid for 7 days"],["15","Valid for 15 days"],["30","Valid for 30 days"],["45","Valid for 45 days"],["60","Valid for 60 days"],["90","Valid for 90 days"]]','quote:[["7","Válida por 7 días"],["15","Válida por 15 días"],["30","Válida por 30 días"],["45","Válida por 45 días"],["60","Válida por 60 días"],["90","Válida por 90 días"]]')
R('invoice:[["0","Due on receipt"],["7","Net 7"],["15","Net 15"],["30","Net 30"],["45","Net 45"],["60","Net 60"]]','invoice:[["0","Al recibir"],["7","Neto 7"],["15","Neto 15"],["30","Neto 30"],["45","Neto 45"],["60","Neto 60"]]')
R('var DEFAULT_TERMS_TEXT="This quote is valid until the date shown. Prices cover the scope described above. Work outside that scope is quoted separately and starts only after you approve it in writing.";','var DEFAULT_TERMS_TEXT="Esta cotización es válida hasta la fecha indicada. Los precios cubren el alcance descrito arriba. El trabajo fuera de ese alcance se cotiza aparte y empieza solo después de su aprobación por escrito.";')
R('lbl=st==="Paid"?"Total paid":st==="Void"?"Total (void)":"Total due"','lbl=st==="Pagada"?"Total pagado":st==="Anulada"?"Total (anulada)":"Total a pagar"')
R('!(v==="Paid"||v==="Void"||v==="Accepted"||v==="Declined")','!(v==="Pagada"||v==="Anulada"||v==="Aceptada"||v==="Rechazada")')
R('"Check the fields marked in red: numbers only, up to 3 decimals for quantity and 4 for unit price, tax up to 100%."','"Revisa los campos en rojo: solo números, hasta 3 decimales en cantidad y 4 en precio unitario, impuesto hasta 100%."')
R('textContent="Saved on this browser. Download the file to keep a copy."','textContent="Guardado en este navegador. Descarga el archivo para conservar una copia."')
R('textContent="This browser would not save your draft. Download the file before you leave."','textContent="Este navegador no guardó tu borrador. Descarga el archivo antes de salir."')
R('prefixQ:"Q-",prefixI:"INV-"','prefixQ:"COT-",prefixI:"FAC-"')
R('toast("New "+state.type+" started. Your company details were kept.","Undo",','toast((state.type==="quote"?"Nueva cotización":"Nueva factura")+" iniciada. Se conservaron los datos de tu empresa.","Deshacer",')
R('aria-label="Description" placeholder="e.g. Backend API development"','aria-label="Descripción" placeholder="Ej. Desarrollo de API"')
R('aria-label="Quantity"','aria-label="Cantidad"')
R('aria-label="Unit" placeholder="ea"','aria-label="Unidad" placeholder="u"')
R('aria-label="Unit price"','aria-label="Precio unitario"')
R('aria-label="Remove line" title="Remove line"','aria-label="Quitar línea" title="Quitar línea"')
R("'<!doctype html><html lang=\"en\"><head>","'<!doctype html><html lang=\"es\"><head>")
R('<span>Print this page and choose Save as PDF to get a PDF.</span><button type="button" onclick="window.print()">Print or save as PDF</button>','<span>Imprime esta página y elige Guardar como PDF para obtener el PDF.</span><button type="button" onclick="window.print()">Imprimir o guardar como PDF</button>')
R('toast("Use a logo under 300 KB so the file stays small.")','toast("Usa un logo de menos de 300 KB para que el archivo no pese mucho.")')
R('toast("That image could not be read.")','toast("No se pudo leer esa imagen.")')
a=d.t.index('function sampleDoc(){'); b=d.t.index('function newDoc(){')
d.t=d.t[:a]+'''function sampleDoc(){
  var o=baseSettings();
  o.type="quote";o.sample=true;
  o.cName="VERSA Technologies LLC";o.footer="Gracias por la oportunidad.";o.quoteTerms=DEFAULT_TERMS_TEXT;
  o.number="COT-0001";o.status="Pendiente";o.issued=todayStr();o.terms="30";o.due=addDays(o.issued,30);
  o.custName="Cliente de ejemplo";o.custAddress="123 Calle Ejemplo\\nOmaha, NE 68102";
  o.projName="Ejemplo: portal de clientes";
  o.scope="Diseño y desarrollo del portal de clientes descrito en las notas de descubrimiento, más una revisión de seguridad antes del lanzamiento. Texto de ejemplo, reemplázalo.";
  o.lines=[{desc:"Taller de descubrimiento y arquitectura",qty:"1",unit:"gl",price:"2,400.00"},{desc:"Desarrollo de API backend",qty:"80",unit:"h",price:"95.00"},{desc:"Revisión de seguridad (OWASP Top 10)",qty:"1",unit:"gl",price:"1,800.00"}];
  return o;
}
'''+d.t[b:]
# leftovers check
import re
script=d.t[d.t.index('<script>'):]
left=[w for w in ['"Total"','Pending','Accepted','Invoice','Quote "','Saved ','Download','Undo'] if w in script.replace('downloads','').replace('download(','').replace('Download file','')]
print('ES leftover tokens (check):',left)
os.makedirs(OUT+'/es',exist_ok=True)
open(OUT+'/es/index.html','w',encoding='utf-8').write(head+d.t+'</body>\n</html>\n')
print('ok')

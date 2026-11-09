import http from 'node:http';
import {readFile} from 'node:fs/promises';
const files={'/':'index.html','/index.html':'index.html','/style.css':'style.css','/app.js':'app.js'};
http.createServer(async(req,res)=>{const file=files[new URL(req.url,'http://localhost').pathname];if(!file){res.writeHead(404);res.end();return;}try{const body=await readFile(new URL(file,import.meta.url));res.setHeader('Content-Type',file.endsWith('.css')?'text/css':file.endsWith('.js')?'text/javascript':'text/html; charset=utf-8');res.end(body);}catch{res.writeHead(500);res.end();}}).listen(4318,'127.0.0.1',()=>console.log('Prévia visual: http://localhost:4318'));

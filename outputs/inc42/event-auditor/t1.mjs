import { chromium } from 'playwright';
const b = await chromium.launch({headless:true, channel:'chrome'});
const p = await (await b.newContext()).newPage();
p.on('response', async r => {
  if (r.url() === 'https://inc42.com/') {
    const h = r.headers();
    console.log('status', r.status());
    console.log('content-type      :', h['content-type']);
    console.log('content-disposition:', h['content-disposition']);
    console.log('content-encoding  :', h['content-encoding']);
    console.log('cf-mitigated      :', h['cf-mitigated']);
    console.log('server            :', h['server']);
  }
});
p.on('request', r => { if (r.url()==='https://inc42.com/') console.log('req headers:', JSON.stringify(r.headers(), null, 1).slice(0,900)); });
try { await p.goto('https://inc42.com/', {waitUntil:'commit', timeout:25000}); } catch(e){ console.log('ERR', String(e).split('\n')[0]); }
await b.close(); process.exit(0);


async function loadIndex(){
  const res = await fetch('/search_index.json', {cache: 'no-store'});
  if(!res.ok) throw new Error('search_index.json not found');
  return await res.json();
}
function tokenize(q){ return q.toLowerCase().split(/\s+/).filter(Boolean); }
function scoreEntry(entry, terms){
  let score = 0;
  const title=(entry.title||'').toLowerCase();
  const summary=(entry.summary||'').toLowerCase();
  const content=(entry.content||'').toLowerCase();
  const tags=(entry.tags||[]).map(t=>t.toLowerCase());
  for(const t of terms){
    if(title.includes(t)) score+=3;
    if(summary.includes(t)) score+=2;
    if(content.includes(t)) score+=1;
    if(tags.some(x=>x.includes(t))) score+=2;
  }
  if(entry.date_iso){
    const days=(Date.now()-new Date(entry.date_iso).getTime())/86400000;
    if(days<60) score+=1;
  }
  return score;
}
function highlight(text, terms){
  let out=text||'';
  for(const t of terms){
    const re=new RegExp('('+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');
    out=out.replace(re,'<mark>$1</mark>');
  }
  return out;
}
function renderResults(entries, terms){
  const box=document.getElementById('results');
  box.innerHTML='';
  if(!terms.length){ box.innerHTML='<p class="muted">Type to search posts…</p>'; return; }
  if(!entries.length){ box.innerHTML='<p class="muted">No matches.</p>'; return; }
  for(const e of entries){
    const item=document.createElement('div');
    item.className='result';
    const title=highlight(e.title||'',terms);
    const snippet=highlight(e.summary||e.content?.slice(0,200)||'',terms);
    const date=e.date||e.date_iso||'';
    const tags=(e.tags||[]).map(t=>`<span class="tag">${t}</span>`).join(' ');
    item.innerHTML=`
      <a href="${e.url}">${title}</a>
      <div class="muted">${date}</div>
      <div class="snippet">${snippet}</div>
      <div class="tags">${tags}</div>
    `;
    box.appendChild(item);
  }
}
async function initSearch(){
  try{
    const index=await loadIndex();
    const input=document.getElementById('q');
    const doSearch=()=>{
      const terms=tokenize(input.value);
      const scored=index.map(e=>({e,s:scoreEntry(e,terms)}))
        .filter(x=>x.s>0||terms.length===0)
        .sort((a,b)=>b.s-a.s)
        .map(x=>x.e);
      renderResults(scored,terms);
    };
    input.addEventListener('input',doSearch);
    doSearch();
  }catch(err){
    const box=document.getElementById('results');
    box.innerHTML='<p class="muted">Search index not found. Add /search_index.json.</p>';
    console.error(err);
  }
}
document.addEventListener('DOMContentLoaded',initSearch);

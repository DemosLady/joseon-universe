'use strict';
const ROUTES=(()=>{
  const chapterKO=['tistory_ch1_blood_and_fog.html','tistory_ch2_ink_and_embers.html','tistory_ch3_ash_and_seed.html','tistory_ch4_salt_and_waves.html','tistory_ch5_sea_and_bones.html','tistory_ch6_island_and_stars.html','chapter7.html','chapter8.html','chapter9.html'];
  const archiveFiles={summary:'story.html',songs:'songs.html',search:'search.html',timeline:'timeline.html',ledger:'ledger.html',history:'references.html',book:'book.html',contact:'contact.html'};
  const records=[];
  function add(lang,view,id,path){records.push({lang,view,id:String(id||''),path})}
  for(const lang of ['ko','en']){const p=lang==='en'?'/en/':'/';add(lang,'story',1,p);for(let n=2;n<=9;n++)add(lang,'story',n,p+'listen/ch'+n+'.html');for(let n=1;n<=9;n++)add(lang,'chapter',n,lang==='ko'?'/'+chapterKO[n-1]:p+(n<7?'ch':'chapter')+n+'.html');for(const s of TRACKS)add(lang,'song',s.id,p+'songs/'+s.id+'.html');for(const id of [...Array.from({length:10},(_,n)=>'ch'+n),'hanpan'])add(lang,'album',id,p+'lyrics-'+id+'.html');add(lang,'characters','all',p+'characters.html');for(const person of PEOPLE)add(lang,'character',person.id,p+'characters/'+person.id+'.html');for(const place of Object.keys(ARCHIVE.places.en))add(lang,'map',place,p+(place==='hanyang'?'map.html':'places/'+place+'.html'));for(const [id,file] of Object.entries(archiveFiles))add(lang,'archive',id,p+file);add(lang,'worlds','',p+'worlds.html');}
  const byPath=new Map(records.map(r=>[r.path,r]));
  function path(lang,view,id=''){if(view==='characters'&&PEOPLE.some(p=>p.id===id))view='character';const record=records.find(r=>r.lang===lang&&r.view===view&&(r.id===String(id)||(view==='characters')));if(!record)return lang==='en'?'/en/':'/';return record.path+(view==='characters'&&['fire','sea','iron'].includes(id)?'?trilogy='+id:'')}
  function parse(pathname){let path=pathname.replace(/\/index\.html$/,'/');return byPath.get(path)||byPath.get(path+'.html')||byPath.get(path.replace(/\/$/,'')+'.html')||null}
  function legacy(hash,fallback='en'){if(!/^#(?:ko\/|en\/|story\/|chapter\/|characters\/|map\/|archive\/|album\/|song\/|worlds)/.test(hash))return null;const [route,q='']=hash.slice(1).split('?'),bits=route.split('/');const lang=['ko','en'].includes(bits[0])?bits.shift():fallback;let [view,id='']=bits;return path(lang,view,id)+(q?(path(lang,view,id).includes('?')?'&':'?')+q:'')}
  return {records,path,parse,legacy};
})();

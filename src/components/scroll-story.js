/** Scroll position drives the pinned scene's camera and editorial chapters. */
export function mountScrollStory(intro){
 const wrapper=document.createElement('div');wrapper.id='home-scroll-story';intro.replaceWith(wrapper);wrapper.append(intro);
 const chapters=[['Context changes everything.','Movement can distort an optical signal. See why PulseCast considers signal quality before showing an illustrative score.','Explore the signals','overview'],['Evidence you can inspect.','Public HbA1c labels, illustrative wearable replay, and clear limits. Every layer has a source and a boundary.','Review the evidence','validation'],['A clearer view. For everyone.','Explore the public cohort in doctor view, or the assigned demo profile in patient view. Research made understandable.','Enter PulseCast','overview']];
 const nodes=chapters.map(([title,copy,label,route])=>{const node=document.createElement('div');node.className='scroll-story-copy';node.innerHTML=`<h2>${title}</h2><p>${copy}</p><a class="story-link" href="#/${route}">${label} ↗</a>`;intro.append(node);return node});
 const cue=document.createElement('div');cue.className='scroll-cue';cue.textContent='Scroll to explore ↓';intro.append(cue);
 const progress=document.createElement('div');progress.className='story-progress';progress.setAttribute('aria-hidden','true');progress.innerHTML='<i></i><i></i><i></i><i></i>';intro.append(progress);
 const reduced=matchMedia('(prefers-reduced-motion:reduce)');let queued=false;
 const opacity=(position,index)=>Math.max(0,1-Math.abs(position-index)*2.3);
 function update(){queued=false;if(reduced.matches)return;const range=wrapper.offsetHeight-innerHeight;const p=Math.max(0,Math.min(1,-wrapper.getBoundingClientRect().top/Math.max(1,range)));const chapter=p*3;intro.querySelector('canvas').dataset.progress=String(p);
  const original=intro.querySelector('.cinema-content'),wordmark=intro.querySelector('.cinema-wordmark'),video=intro.querySelector('video');original.style.opacity=String(opacity(chapter,0));original.style.visibility=opacity(chapter,0)>.03?'visible':'hidden';original.setAttribute('aria-hidden',String(opacity(chapter,0)<.03));original.style.transform=`translateY(${-p*140}px)`;original.style.pointerEvents=p<.2?'auto':'none';wordmark.style.opacity=String(Math.max(0,1-p*4));wordmark.style.transform=`translateY(${-p*260}px) scale(${1+p*.3})`;
  video.style.transform=`scale(${1+p*.6}) translate(${Math.sin(p*Math.PI)*-7}%,${p*-6}%)`;video.style.filter=`saturate(${1-p*.3})`;
  nodes.forEach((node,index)=>{const alpha=opacity(chapter,index+1);node.style.opacity=String(alpha);node.setAttribute('aria-hidden',String(alpha<.03));node.style.transform=`translate(-50%,calc(-50% + ${(index+1-chapter)*80}px))`;node.style.visibility=alpha>.03?'visible':'hidden';node.querySelector('a').tabIndex=alpha>.5?0:-1});
  original.querySelectorAll('button').forEach(b=>b.tabIndex=p<.2?0:-1);progress.querySelectorAll('i').forEach((dot,index)=>dot.classList.toggle('active',index===Math.round(chapter)));cue.style.opacity=String(Math.max(0,1-p*7));
 }
 function schedule(){if(!queued){queued=true;requestAnimationFrame(update)}}window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);window.addEventListener('hashchange',schedule);reduced.addEventListener('change',()=>{[intro.querySelector('.cinema-content'),intro.querySelector('.cinema-wordmark'),...nodes].forEach(node=>{node.style.cssText='';node.removeAttribute('aria-hidden')});update()});update();
 return wrapper;
}

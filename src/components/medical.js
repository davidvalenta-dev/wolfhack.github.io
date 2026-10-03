import {history} from '../data/cohort.js';
import {askAgent} from '../services/agent.js';
import {mountTheme} from './theme.js';
let typedQuestion='';
let savedAnswer='',savedContext='',pending=false,requestVersion=0;
/** Presentation-only audience switching for public demo records; not authentication. */
export function medicalWorkspace({audience,participant,minute,onSwitch,onQuestionFocus}){
 document.body.dataset.audience=audience;
 document.querySelector('.motion-toggle')?.remove();
 document.querySelector('.video-quality')?.remove();
 const backgroundVideo=document.querySelector('.cinema-video');if(backgroundVideo)backgroundVideo.loop=true;
 const workspace=document.querySelector('.workspace');workspace.innerHTML=`<div class="audience-tabs" role="group" aria-label="Workspace view"><button data-audience="doctor" aria-pressed="${audience==='doctor'}"><i class="ti ti-stethoscope" aria-hidden="true"></i> Doctor view</button><button data-audience="patient" aria-pressed="${audience==='patient'}"><i class="ti ti-heart" aria-hidden="true"></i> Patient view</button></div>`;
 workspace.querySelectorAll('button').forEach(b=>b.onclick=()=>onSwitch(b.dataset.audience));
 mountTheme();
 document.querySelector('.brand-mark').textContent='✚';
 const hero=document.querySelector('.cinema-content');hero.querySelector('h2').textContent=audience==='doctor'?'See the signal. Understand the story.':'Your signals. Your story.';
 hero.querySelector('p').textContent=audience==='doctor'?'Explore wearable physiology with the context to ask better questions.':'Explore your wearable profile with clear explanations of what the signals mean.';
 document.querySelector('.film-label').textContent='Wearable research, in perspective';
 document.querySelector('.editorial').hidden=false;
 document.querySelector('#discover-science').onclick=()=>document.dispatchEvent(new Event('pulsecast:demo'));
 const heading=document.querySelector('.page-head h1');if(document.querySelector('#play'))heading.textContent=audience==='doctor'?'Patient overview':'My health overview';
 document.querySelector('.page-head p').textContent=audience==='doctor'?'Review sensor trends and supporting evidence for the selected research participant.':'Your assigned demo profile · Participant 004';
 if(audience==='patient'){
  document.querySelector('[data-tab="Cohort"]').remove();document.querySelector('.participant-select').remove();
  document.querySelector('[data-tab="Overview"]').textContent='My overview';
  document.querySelector('[data-tab="Validation"]').textContent='My evidence';
  document.querySelector('.breadcrumb').textContent='Patient workspace / My profile';
 }else document.querySelector('[data-tab="Cohort"]').textContent='Patient cohort';
 document.querySelector('.header-right').innerHTML=`<span class="status-dot"></span>${audience==='doctor'?'Clinical research workspace':'Personal demo workspace'}`;
 const note=document.createElement('div');note.className='role-note';note.textContent=audience==='patient'?'Showing only your assigned demo profile. This view switch is a demo; real patient access requires authenticated server-side permissions.':'Doctor workspace · Public research cohort · Simulated wearable trends';document.querySelector('.notice').after(note);
 if(!document.querySelector('#play'))return;
 const values=history(participant,minute);
 const charts=document.createElement('section');charts.className='clinical-charts';charts.setAttribute('aria-label','Patient physiological trend charts');
 const configs=[['Heart rate','hr','bpm','#147dba',55,100],['Heart rate variability','hrv','ms','#299b91',20,65],['Skin conductance','eda','µS','#7d73b5',.5,2.5],['Skin temperature','temp','°C','#d29158',31,34]];
 charts.innerHTML=configs.map(([name,key,unit,color,min,max])=>{const coordinates=values.map((v,i)=>`${40+i/90*450},${145-(v[key]-min)/(max-min)*115}`).join(' ');const current=values.at(-1)[key];return `<article class="card clinical-chart"><div class="section-head"><h2>${name}</h2><span class="chart-current" style="color:${color}">${current} <small>${unit}</small></span></div><svg viewBox="0 0 520 185" role="img" aria-label="${name} synthetic trend for participant ${participant}">${[0,1,2].map(i=>`<line x1="40" x2="490" y1="${30+i*57.5}" y2="${30+i*57.5}" stroke="#e4edf3" stroke-dasharray="3 4"/><text x="0" y="${34+i*57.5}" fill="#8198aa" font-size="9">${(max-i*(max-min)/2).toFixed(key==='eda'||key==='temp'?1:0)}</text>`).join('')}<polyline points="${coordinates}" stroke="${color}" stroke-width="2.5" fill="none" stroke-linejoin="round"/>${[0,30,60,90].map(t=>`<text x="${40+t/90*450}" y="177" fill="#8198aa" font-size="9">${10+Math.floor(t/60)}:${String(t%60).padStart(2,'0')}</text>`).join('')}</svg><div class="chart-caption"><span>● Synthetic replay</span><span>Session ${participant}</span></div></article>`}).join('');
 document.querySelector('.two-col.lower').before(charts);
 const assistant=document.querySelector('.explain');
 assistant.querySelector('h2').textContent=audience==='doctor'?'PulseCast Assistant':'PulseCast Assistant';
 assistant.querySelector('.assistant-footer').textContent='PulseCast Assistant · Research demo';
 const context=`${audience}:${participant}`;
 if(savedContext!==context){savedAnswer='';typedQuestion='';savedContext=context;pending=false;requestVersion++;}
 const answer=assistant.querySelector('.answer');answer.textContent=savedAnswer||'What would you like to understand? Ask about this profile, its signal quality, or the limits of the evidence.';
 const form=document.createElement('form');form.className='agent-form';form.innerHTML='<input aria-label="Question for insight assistant" placeholder="Ask about these signals…" maxlength="2000" required><button type="submit">Ask ↗</button>';
 assistant.querySelector('.assistant-footer').before(form);
 const questionInput=form.querySelector('input');questionInput.value=typedQuestion;questionInput.oninput=()=>{typedQuestion=questionInput.value;};questionInput.onfocus=()=>onQuestionFocus?.();
 async function submit(question){if(pending)return;pending=true;const version=++requestVersion;savedAnswer='Connecting the signals…';answer.textContent=savedAnswer;form.querySelector('button').disabled=true;try{const result=await askAgent({subject_id:participant,question,audience,minute});if(version===requestVersion)savedAnswer=result.answer;}catch(error){if(version===requestVersion)savedAnswer=error.message;}finally{if(version===requestVersion){pending=false;const visible=document.querySelector('.explain .answer');if(visible)visible.textContent=savedAnswer;const button=document.querySelector('.agent-form button');if(button)button.disabled=false;}}}
 form.onsubmit=e=>{e.preventDefault();submit(form.querySelector('input').value.trim());};
 assistant.querySelectorAll('[data-q]').forEach(button=>button.onclick=()=>submit(button.textContent.replace('↗','').trim()));
 document.querySelectorAll('.spark').forEach(el=>{el.innerHTML='<svg viewBox="0 0 90 25" aria-hidden="true"><polyline points="0,18 10,14 18,17 30,5 38,12 50,9 62,15 75,7 90,10" stroke="#32a8ad" fill="none" stroke-width="2"/></svg>'});
}

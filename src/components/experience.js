import {mountScrollStory} from './scroll-story.js';
import {mountSignalField} from './signal-field.js';
/** Existing brand retained. Media is illustrative, not a study participant or device claim. */
let retainedIntro, retainedEditorial;
export function mountExperience(){
 const app=document.querySelector('#app');
 if(retainedIntro){app.prepend(retainedIntro);app.querySelector('main').before(retainedEditorial);return;}
 const intro=document.createElement('section');intro.className='cinema';intro.id='home';
 intro.innerHTML=`<canvas class="signal-field" aria-hidden="true"></canvas><div class="cinema-wordmark" aria-hidden="true">PULSECAST</div><div class="cinema-content"><span class="film-label">Wearable research, in perspective</span><h2>See the signal. Understand the story.</h2><p>Explore wearable physiology with the context to ask better questions.</p><div class="hero-actions"><button id="enter-dashboard">Explore PulseCast <i class="ti ti-arrow-up-right" aria-hidden="true"></i></button><button id="discover-science">Try the demo <i class="ti ti-player-play" aria-hidden="true"></i></button></div></div><figure class="hero-media"><div class="media-frame"><video class="cinema-video" muted loop playsinline preload="metadata" aria-hidden="true" poster="https://images.pexels.com/videos/8325857/analysis-analyzing-biochemistry-biology-8325857.jpeg?auto=compress&dpr=1&h=1080&w=1920"></video></div><figcaption><span>Illustrative research footage</span><a class="photo-credit" href="https://www.pexels.com/video/laboratory-tools-and-equipment-8325857/" target="_blank" rel="noreferrer">Kindel Media / Pexels</a></figcaption></figure>`;
 mountSignalField(intro.querySelector('canvas'));
 const video=intro.querySelector('video');video.muted=true;
 if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches&&!navigator.connection?.saveData){
  const constrained=window.matchMedia('(max-width: 700px)').matches;
  video.src=constrained?'https://videos.pexels.com/video-files/9244196/9244196-hd_1920_1080_25fps.mp4':'https://videos.pexels.com/video-files/8325857/8325857-uhd_3840_2160_30fps.mp4';
  if(constrained){const credit=intro.querySelector('.photo-credit');credit.textContent='Mikhail Nilov / Pexels';credit.href='https://www.pexels.com/video/a-person-using-microscope-in-the-laboratory-9244196/';}
  video.play().catch(()=>{});
 }
 const editorial=document.createElement('section');editorial.className='editorial';
 editorial.innerHTML=`<div class="research-intro"><span>16 participant profiles from open research</span><p>Observed HbA1c labels. Illustrative wearable replay. Model validation pending.</p><a href="https://physionet.org/content/big-ideas-glycemic-wearable/1.1.3/" target="_blank" rel="noreferrer">Explore the dataset <i class="ti ti-arrow-up-right" aria-hidden="true"></i></a></div>`;
 app.prepend(intro);app.querySelector('main').before(editorial);
 intro.querySelector('#enter-dashboard').onclick=()=>{location.hash='/overview';};
 intro.querySelector('#discover-science').onclick=()=>document.dispatchEvent(new Event('pulsecast:demo'));
 retainedIntro=mountScrollStory(intro);retainedEditorial=editorial;
}

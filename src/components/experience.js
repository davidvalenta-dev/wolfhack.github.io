/** Original visual design. Stock film and photos illustrate activity, not study participants. */
let retainedIntro, retainedEditorial;
export function mountExperience(){
 const app=document.querySelector('#app');
 if(retainedIntro){app.prepend(retainedIntro);app.querySelector('main').before(retainedEditorial);return;}
 const intro=document.createElement('section');intro.className='cinema';intro.id='home';
 intro.innerHTML=`<div class="cinema-photo"></div><video class="cinema-video" muted loop playsinline preload="metadata" aria-hidden="true" poster="https://images.pexels.com/videos/8325857/analysis-analyzing-biochemistry-biology-8325857.jpeg?auto=compress&dpr=1&h=1080&w=1920"></video><div class="cinema-shade"></div><div class="cinema-content"><span class="film-label"><i></i> THE NEXT PERSPECTIVE IN WEARABLE RESEARCH</span><h2>See the signal.<br><em>Understand the story.</em></h2><p>Every heartbeat has context. Bring it into focus.<br>A thoughtfully connected view of human physiology.</p><div class="hero-actions"><button id="enter-dashboard">Explore PulseCast <span>↗</span></button><button id="discover-science">Try the demo <span>▷</span></button></div><span class="hero-footnote">Built for WolfHacks 2026 · Research prototype</span></div><div class="hero-preview" aria-label="Illustrative signal preview"><div class="preview-top"><span><i></i> SIGNAL INTELLIGENCE</span><span>DEMO / 004</span></div><div class="preview-wave"><svg viewBox="0 0 560 90" aria-hidden="true"><defs><linearGradient id="hero-wave"><stop stop-color="#9af3dc"/><stop offset="1" stop-color="#98baff"/></linearGradient></defs><path d="M0 48H55L65 43L76 52L90 14L104 79L117 48H170L184 43L195 53L209 12L223 78L237 48H290L301 42L315 55L327 12L341 79L355 48H410L425 42L437 52L451 14L464 78L478 48H560"/></svg></div><div class="preview-stats"><div><span>HEART RATE</span><strong>75 <small>bpm</small></strong></div><div><span>VARIABILITY</span><strong>46 <small>ms</small></strong></div><div><span>SIGNAL QUALITY</span><strong>94 <small>%</small></strong></div><span class="preview-tag">Illustrative preview</span></div></div><div class="hero-bottom"><span>DESIGNED TO REVEAL. BUILT TO EXPLAIN.</span><a class="photo-credit" href="https://www.pexels.com/video/laboratory-tools-and-equipment-8325857/" target="_blank" rel="noreferrer">Film by Kindel Media / Pexels ↗</a></div>`;
 const video=intro.querySelector('video');video.muted=true;
 if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches){
  const constrained=window.matchMedia('(max-width: 700px)').matches||navigator.connection?.saveData;
  video.src=constrained?'https://videos.pexels.com/video-files/9244196/9244196-hd_1920_1080_25fps.mp4':'https://videos.pexels.com/video-files/8325857/8325857-uhd_3840_2160_30fps.mp4';
  if(constrained){const credit=intro.querySelector('.photo-credit');credit.textContent='Film by Mikhail Nilov / Pexels ↗';credit.href='https://www.pexels.com/video/a-person-using-microscope-in-the-laboratory-9244196/';}
  video.play().catch(()=>{});video.addEventListener('playing',()=>video.classList.add('loaded'));
 }
 const editorial=document.createElement('section');editorial.className='editorial';
 editorial.innerHTML=`<div class="intro-strip"><div><span class="strip-number">01</span><strong>See the whole session.</strong><p>Replay physiology. Find the moments that matter.</p></div><div><span class="strip-number">02</span><strong>Question the signal.</strong><p>Motion-aware confidence, at every step.</p></div><div><span class="strip-number">03</span><strong>Follow the evidence.</strong><p>Clear sources. Honest limitations. Better questions.</p></div></div>`;
 app.prepend(intro);app.querySelector('main').before(editorial);
 intro.querySelector('#enter-dashboard').onclick=()=>document.querySelector('main').scrollIntoView({behavior:'smooth'});
 intro.querySelector('#discover-science').onclick=()=>document.dispatchEvent(new Event('pulsecast:demo'));
 retainedIntro=intro;retainedEditorial=editorial;
}

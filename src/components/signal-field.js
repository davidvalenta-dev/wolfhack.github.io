/** Original projected signal terrain, animated without external artwork. */
export function mountSignalField(canvas){
 const context=canvas.getContext('2d');if(!context)return;
 const reduced=matchMedia('(prefers-reduced-motion:reduce)');let width=0,height=0,frame=0,visible=true;
 const resize=()=>{const box=canvas.getBoundingClientRect();width=box.width;height=box.height;const dpr=Math.min(devicePixelRatio,1.5);canvas.width=width*dpr;canvas.height=height*dpr;context.setTransform(dpr,0,0,dpr,0,0);};
 const draw=(time=0)=>{context.clearRect(0,0,width,height);const dark=document.documentElement.dataset.theme==='dark',phase=reduced.matches?0:time*.00013;
  for(let row=0;row<55;row++){const depth=row/54;for(let column=0;column<105;column++){const u=column/104;const x=(u-.5)*width*(.5+depth*1.4)+width*.7;const ridge=Math.sin(u*8+depth*3+phase)*Math.sin(u*3+phase*.5);const y=height*.32+depth*depth*height*.8-ridge*height*.23*depth;const flow=Math.abs(Math.sin(u*12+depth*5-phase*2));const bright=flow<.12;context.fillStyle=dark?(bright?`rgba(181,242,209,${.5+depth*.5})`:`rgba(70,174,222,${.1+depth*.5})`):(bright?`rgba(13,122,116,${.25+depth*.5})`:`rgba(25,118,157,${.08+depth*.3})`);context.beginPath();context.arc(x,y,bright?1.2+depth*2:.4+depth*1.25,0,Math.PI*2);context.fill();}}
  if(visible&&!reduced.matches)frame=requestAnimationFrame(draw);
 };
 const start=()=>{cancelAnimationFrame(frame);resize();draw(performance.now());};new ResizeObserver(start).observe(canvas);new MutationObserver(start).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});reduced.addEventListener('change',start);new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;cancelAnimationFrame(frame);if(visible)draw(performance.now())}).observe(canvas);start();
}

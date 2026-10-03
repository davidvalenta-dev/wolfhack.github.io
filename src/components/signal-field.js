/** Original canvas signal landscape. No copied Remix artwork or tracking. */
export function mountSignalField(canvas){
 const context=canvas.getContext('2d');if(!context)return;
 const reduced=matchMedia('(prefers-reduced-motion:reduce)');let width=0,height=0,frame=0,visible=true;
 const resize=()=>{const box=canvas.getBoundingClientRect();width=box.width;height=box.height;const dpr=Math.min(devicePixelRatio,2);canvas.width=width*dpr;canvas.height=height*dpr;context.setTransform(dpr,0,0,dpr,0,0);};
 const draw=(time=0)=>{context.clearRect(0,0,width,height);const dark=document.documentElement.dataset.theme==='dark';const phase=reduced.matches?0:time*.00015;
  for(let row=0;row<38;row++){const depth=row/37;const y=height*.45+depth*depth*height*.55;for(let column=0;column<100;column++){const x=(column/99-.5)*width*1.5+width/2;const wave=Math.sin(column*.09+row*.15+phase)*35*depth+Math.sin(column*.21-phase)*18*depth;const pulse=Math.exp(-Math.pow((column/99-.5)*9,2))*Math.sin(column*.45-phase*3)*50*depth;const radius=.45+depth*1.6;context.fillStyle=dark?`rgba(${row%7===0?'148,226,199':'79,190,232'},${.15+depth*.55})`:`rgba(15,107,146,${.1+depth*.45})`;context.beginPath();context.arc(x,y+wave+pulse,radius,0,Math.PI*2);context.fill();}}
  if(visible&&!reduced.matches)frame=requestAnimationFrame(draw);
 };
 const start=()=>{cancelAnimationFrame(frame);resize();draw(performance.now());};
 new ResizeObserver(start).observe(canvas);new MutationObserver(start).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});reduced.addEventListener('change',start);
 new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;cancelAnimationFrame(frame);if(visible)draw(performance.now())}).observe(canvas);start();
}

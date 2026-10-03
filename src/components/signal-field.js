/** Original 3D heart point cloud. Scroll progress controls its camera. */
export function mountSignalField(canvas){
 const context=canvas.getContext('2d');if(!context)return;
 const reduced=matchMedia('(prefers-reduced-motion:reduce)');let width=0,height=0,frame=0,visible=true;
 const points=[];
 for(let ring=1;ring<48;ring++){const phi=ring/48*Math.PI;for(let sample=0;sample<110;sample++){const t=sample/110*Math.PI*2;const r=Math.sin(phi);points.push({x:16*Math.pow(Math.sin(t),3)*r,y:-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t))*r,z:8*Math.cos(phi)*Math.sin(t/2),tone:ring%9===0});}}
 const resize=()=>{const box=canvas.getBoundingClientRect();width=box.width;height=box.height;const dpr=Math.min(devicePixelRatio,1.5);canvas.width=width*dpr;canvas.height=height*dpr;context.setTransform(dpr,0,0,dpr,0,0);};
 const draw=(time=0)=>{context.clearRect(0,0,width,height);const p=Number(canvas.dataset.progress||0),phase=reduced.matches?0:p*Math.PI*1.6+Math.sin(time*.0002)*.05;const angle=phase-.3,tilt=-.12+p*.35,scale=Math.min(width,height)*(width<700?.024:.027)*(1+p*.32);const centerX=width*(.65-p*.18),centerY=height*(.67-p*.04);const cos=Math.cos(angle),sin=Math.sin(angle);
  const transformed=points.map(v=>{const x=v.x*cos+v.z*sin,z=-v.x*sin+v.z*cos,y=v.y*Math.cos(tilt)-z*Math.sin(tilt);return{x,y,z,tone:v.tone}}).sort((a,b)=>a.z-b.z);
  transformed.forEach(v=>{const perspective=65/(65-v.z);const alpha=.2+(v.z+17)/34*.65;context.fillStyle=v.tone?`rgba(166,244,208,${alpha})`:`rgba(102,209,239,${alpha})`;context.beginPath();context.arc(centerX+v.x*scale*perspective,centerY+v.y*scale*perspective,Math.max(.65,(1+v.z/25)*1.5),0,Math.PI*2);context.fill()});
  for(let row=0;row<16;row++){const depth=row/15;for(let col=0;col<70;col++){const x=col/69*width,y=height*.75+depth*depth*height*.4+Math.sin(col*.11+phase)*12*depth;context.fillStyle=`rgba(85,174,218,${.08+depth*.3})`;context.beginPath();context.arc(x,y,.5+depth,0,Math.PI*2);context.fill()}}
  if(visible&&!reduced.matches)frame=requestAnimationFrame(draw);
 };
 const start=()=>{cancelAnimationFrame(frame);resize();draw(performance.now());};new ResizeObserver(start).observe(canvas);reduced.addEventListener('change',start);new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;cancelAnimationFrame(frame);if(visible)draw(performance.now())}).observe(canvas);start();
}

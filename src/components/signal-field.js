/** GPU-rendered morphing particle sculpture. Deterministic targets, scroll-driven assembly. */
export function mountSignalField(canvas){
 const gl=canvas.getContext('webgl',{alpha:true,antialias:false,powerPreference:'high-performance'});if(!gl){canvas.closest('.cinema')?.classList.add('no-particles');return;}
 const mobile=innerWidth<700,count=mobile?60000:200000;
 const shader=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);return s};
 const program=gl.createProgram();gl.attachShader(program,shader(gl.VERTEX_SHADER,`
 precision highp float;attribute vec3 aHeart,aHelix,aWave,aBurst;attribute float aSeed;
 uniform float uProgress,uTime,uAspect,uSize;
 varying vec3 vColor;varying float vAlpha;
 void main(){float stage=uProgress*3.;float index=floor(min(stage,2.999));float t=fract(min(stage,2.999));t=smoothstep(0.,1.,t);
 vec3 from=aHeart;vec3 dest=aHelix;if(index>0.5){from=aHelix;dest=aWave;}if(index>1.5){from=aWave;dest=aHeart*.85;}
 float dissolve=sin(t*3.14159265);vec3 p=mix(from,dest,t)+aBurst*dissolve*.85;p.x+=sin(p.y*3.+uProgress*10.)*dissolve*.4;p.z+=cos(p.x*4.)*dissolve*.2;
 float angle=uProgress*2.5+sin(uTime*.12)*.07;float c=cos(angle),s=sin(angle);p.xz=mat2(c,-s,s,c)*p.xz;
 p.y+=sin(uTime*.5+aSeed*30.)*.015;float depth=3.7-p.z;float zoom=2.2;
 gl_Position=vec4(p.x*zoom/uAspect/depth,p.y*zoom/depth-.15,0.,1.);
 gl_PointSize=clamp(uSize*(1.5+1.5/depth)*(0.65+aSeed),1.,4.);
 vec3 cyan=vec3(.16,.8,1.);vec3 gold=vec3(1.,.8,.25);vec3 pink=vec3(1.,.25,.47);vec3 green=vec3(.25,1.,.65);
 vec3 col=mix(cyan,gold,smoothstep(.05,.4,uProgress));col=mix(col,pink,smoothstep(.4,.7,uProgress));col=mix(col,green,smoothstep(.7,1.,uProgress));
 vColor=mix(col,vec3(1.),pow(aSeed,14.)*.85);vAlpha=(.3+aSeed*.55)*(1.-dissolve*.05);
 }`));gl.attachShader(program,shader(gl.FRAGMENT_SHADER,`
 precision mediump float;varying vec3 vColor;varying float vAlpha;
 void main(){float d=length(gl_PointCoord-.5)*2.;if(d>1.)discard;float glow=pow(1.-d,1.5);gl_FragColor=vec4(vColor,vAlpha*glow);}`));gl.linkProgram(program);gl.useProgram(program);
 let seed=91823;const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296};
 const heart=new Float32Array(count*3),helix=new Float32Array(count*3),wave=new Float32Array(count*3),burst=new Float32Array(count*3),seeds=new Float32Array(count);
 for(let i=0;i<count;i++){const j=i*3,t=random()*Math.PI*2,phi=Math.acos(random()*2-1),r=Math.sin(phi),v=random(),strand=i%2?Math.PI:0;
 heart[j]=Math.pow(Math.sin(t),3)*r;heart[j+1]=(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t))/16*r;heart[j+2]=Math.cos(phi)*.4*Math.sin(t/2);
 const a=v*Math.PI*8+strand,thickness=(random()-.5)*.09;
 helix[j]=Math.cos(a)*(.52+thickness);helix[j+1]=(v-.5)*2.35;helix[j+2]=Math.sin(a)*(.52+thickness);
 if(i%7===0){const rung=Math.floor(v*24)/24*Math.PI*8;const f=random()*2-1;helix[j]=Math.cos(rung)*.52*f;helix[j+2]=Math.sin(rung)*.52*f;}
 const u=random()*Math.PI*2,b=random()*Math.PI*2,rr=.72+.22*Math.cos(b*3+u*5);wave[j]=rr*Math.cos(u);wave[j+1]=rr*Math.sin(u);wave[j+2]=.4*Math.sin(b+u*3);
 burst[j]=(random()-.5)*3.8;burst[j+1]=(random()-.5)*3;burst[j+2]=(random()-.5)*3;seeds[i]=random();}
 const attribute=(name,data,size)=>{const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,data,gl.STATIC_DRAW);const location=gl.getAttribLocation(program,name);gl.enableVertexAttribArray(location);gl.vertexAttribPointer(location,size,gl.FLOAT,false,0,0)};
 attribute('aHeart',heart,3);attribute('aHelix',helix,3);attribute('aWave',wave,3);attribute('aBurst',burst,3);attribute('aSeed',seeds,1);
 const uniforms=Object.fromEntries(['uProgress','uTime','uAspect','uSize'].map(name=>[name,gl.getUniformLocation(program,name)]));gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE);gl.clearColor(0,0,0,0);
 const reduced=matchMedia('(prefers-reduced-motion:reduce)');let visible=true,frame=0,lost=false;
 const resize=()=>{const box=canvas.getBoundingClientRect(),dpr=Math.min(devicePixelRatio,1.5);canvas.width=box.width*dpr;canvas.height=box.height*dpr;gl.viewport(0,0,canvas.width,canvas.height);};
 function draw(time=0){if(lost)return;gl.clear(gl.COLOR_BUFFER_BIT);gl.uniform1f(uniforms.uProgress,reduced.matches?0:Number(canvas.dataset.progress||0));gl.uniform1f(uniforms.uTime,reduced.matches?0:time*.001);gl.uniform1f(uniforms.uAspect,canvas.width/Math.max(1,canvas.height));gl.uniform1f(uniforms.uSize,mobile?1.6:2.0);gl.drawArrays(gl.POINTS,0,count);if(visible&&!reduced.matches)frame=requestAnimationFrame(draw);}
 const restart=()=>{cancelAnimationFrame(frame);resize();draw(performance.now())};new ResizeObserver(restart).observe(canvas);new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;cancelAnimationFrame(frame);if(visible)draw(performance.now())}).observe(canvas);reduced.addEventListener('change',restart);canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();lost=true;cancelAnimationFrame(frame)});restart();
}

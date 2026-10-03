/** Persistent appearance preference, defaulting to light on first visit. */
let current='light';
try{current=localStorage.getItem('pulsecast-theme')==='dark'?'dark':'light';}catch{}
export function mountTheme(){
 document.documentElement.dataset.theme=current;
 const button=document.createElement('button');button.className='theme-toggle';button.type='button';
 const refresh=()=>{button.textContent=current==='dark'?'☀ Light mode':'☾ Dark mode';button.setAttribute('aria-label',`Switch to ${current==='dark'?'light':'dark'} mode`);button.setAttribute('aria-pressed',String(current==='dark'));};
 button.onclick=()=>{current=current==='dark'?'light':'dark';document.documentElement.dataset.theme=current;try{localStorage.setItem('pulsecast-theme',current);}catch{}refresh();};refresh();document.querySelector('.workspace').append(button);
}

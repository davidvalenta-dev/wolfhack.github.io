import {mountIcons} from './icons.js';
/** Persistent appearance preference, defaulting to light on first visit. */
let current=window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
try{const saved=localStorage.getItem('pulsecast-theme');if(saved==='dark'||saved==='light')current=saved;}catch{}
export function mountTheme(){
 document.documentElement.dataset.theme=current;
 const button=document.createElement('button');button.className='theme-toggle';button.type='button';
 const refresh=()=>{button.innerHTML=`<i class="ti ti-${current==='dark'?'sun':'moon'}" aria-hidden="true"></i><span>${current==='dark'?'Light mode':'Dark mode'}</span>`;button.setAttribute('aria-label',`Switch to ${current==='dark'?'light':'dark'} mode`);button.setAttribute('aria-pressed',String(current==='dark'));mountIcons(button);};
 button.onclick=()=>{current=current==='dark'?'light':'dark';document.documentElement.dataset.theme=current;try{localStorage.setItem('pulsecast-theme',current);}catch{}refresh();};refresh();document.querySelector('.workspace').append(button);
}

import {mountIcons} from './icons.js';
let current='light';
function applyPreference(){let saved='system';try{saved=localStorage.getItem('pulsecast-theme')||'system';}catch{}current=saved==='system'?(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'):saved;document.documentElement.dataset.theme=current;document.querySelectorAll('.theme-toggle').forEach(refresh);}
function refresh(button){button.innerHTML=`<i class="ti ti-${current==='dark'?'sun':'moon'}" aria-hidden="true"></i><span>${current==='dark'?'Light mode':'Dark mode'}</span>`;button.setAttribute('aria-label',`Switch to ${current==='dark'?'light':'dark'} mode`);button.setAttribute('aria-pressed',String(current==='dark'));mountIcons(button);}
window.addEventListener('pulsecast:theme',applyPreference);
matchMedia('(prefers-color-scheme:dark)').addEventListener('change',applyPreference);
export function mountTheme(){applyPreference();const button=document.createElement('button');button.className='theme-toggle';button.type='button';button.onclick=()=>{try{localStorage.setItem('pulsecast-theme',current==='dark'?'light':'dark');}catch{}window.dispatchEvent(new Event('pulsecast:theme'));};refresh(button);document.querySelector('.workspace').append(button);}

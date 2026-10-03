"use client";
import {useEffect,useState} from 'react';
import UserMenu,{type ThemePreference} from '@/components/ui/user-menu';
import {Activity,BookOpen,Download} from 'lucide-react';
const readTheme=():ThemePreference=>{try{return (localStorage.getItem('pulsecast-theme') as ThemePreference)||'system'}catch{return 'system'}};
export default function UserMenuDemo(){
 const [theme,setTheme]=useState<ThemePreference>(readTheme);
 useEffect(()=>{const update=()=>setTheme(readTheme());window.addEventListener('pulsecast:theme',update);return()=>window.removeEventListener('pulsecast:theme',update)},[]);
 return <UserMenu user={{name:'PulseCast Demo',email:'Public research workspace',plan:'Demo'}} theme={theme} onThemeChange={value=>{localStorage.setItem('pulsecast-theme',value);window.dispatchEvent(new Event('pulsecast:theme'));}} items={[
  {label:'Research overview',icon:<Activity size={16}/>,onSelect:()=>document.querySelector<HTMLButtonElement>('nav [data-tab="Overview"]')?.click()},
  {label:'Methodology',icon:<BookOpen size={16}/>,onSelect:()=>document.querySelector<HTMLButtonElement>('nav [data-tab="Methodology"]')?.click()},
  {label:'Download session brief',icon:<Download size={16}/>,onSelect:()=>{if(!document.querySelector('.export-session'))document.querySelector<HTMLButtonElement>('nav [data-tab="Overview"]')?.click();document.querySelector<HTMLButtonElement>('.export-session')?.click();}}
 ]} onSignOut={()=>{document.dispatchEvent(new Event('pulsecast:demo'));}} signOutLabel="Reset demo"/>;
}

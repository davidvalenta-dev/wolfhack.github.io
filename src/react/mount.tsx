import {createRoot} from 'react-dom/client';
import {HeroScrollDemo} from '@/components/ui/hero-scroll-demo';
import UserMenuDemo from '@/components/ui/user-menu-demo';
import '../styles/tailwind.css';
let scrollHost:HTMLDivElement,menuHost:HTMLDivElement;
/** Retain React islands across the vanilla dashboard's replay renders. */
export function mountReactComponents(){
 if(!scrollHost){scrollHost=document.createElement('div');scrollHost.id='scroll-showcase';createRoot(scrollHost).render(<HeroScrollDemo/>);}
 if(!menuHost){menuHost=document.createElement('div');menuHost.className='react-account';createRoot(menuHost).render(<UserMenuDemo/>);}
 document.querySelector('main')?.before(scrollHost);
 document.querySelector('aside .workspace')?.append(menuHost);
}

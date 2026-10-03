import {ResearchCommand,SessionTimeline,ResearchAccordion} from '@/components/ui/research-explorer';
import {createRoot} from 'react-dom/client';
import {HeroScrollDemo} from '@/components/ui/hero-scroll-demo';
import UserMenuDemo from '@/components/ui/user-menu-demo';
import '../styles/tailwind.css';
let scrollHost:HTMLDivElement,menuHost:HTMLDivElement;
/** Retain React islands across the vanilla dashboard's replay renders. */
let commandHost:HTMLDivElement,faqHost:HTMLDivElement,timelineHost:HTMLDivElement,timelineRoot:ReturnType<typeof createRoot>;
export function mountReactComponents(options:{minute:number;onScene:(minute:number)=>void}){
 if(!scrollHost){scrollHost=document.createElement('div');scrollHost.id='scroll-showcase';createRoot(scrollHost).render(<HeroScrollDemo/>);}
 if(!menuHost){menuHost=document.createElement('div');menuHost.className='react-account';createRoot(menuHost).render(<UserMenuDemo/>);}
 if(!commandHost){commandHost=document.createElement('div');createRoot(commandHost).render(<ResearchCommand/>);faqHost=document.createElement('div');createRoot(faqHost).render(<ResearchAccordion/>);timelineHost=document.createElement('div');timelineRoot=createRoot(timelineHost);}
 document.querySelector('.header-right')?.prepend(commandHost);document.querySelector('.product-story')?.before(faqHost);
 const journey=document.querySelector('.demo-journey');if(journey){journey.replaceWith(timelineHost);timelineRoot.render(<SessionTimeline {...options}/>);}
 document.querySelector('main')?.before(scrollHost);
 document.querySelector('aside .workspace')?.append(menuHost);
}


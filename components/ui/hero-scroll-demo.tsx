"use client";
import {ContainerScroll} from '@/components/ui/container-scroll-animation';
export function HeroScrollDemo(){
 return <section className="flex flex-col overflow-hidden" aria-label="Scroll animation of a clinical research image">
  <ContainerScroll titleComponent={<div className="scroll-title"><p>From observation to understanding</p><h2 className="text-4xl font-semibold text-foreground">A closer look at<br/><span className="text-4xl md:text-[5rem] font-bold mt-1 leading-none">Human signals.</span></h2><p>Scroll to bring the research into focus.</p></div>}>
   <img src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1800&q=85" alt="Illustrative clinician using a mobile device with a stethoscope" width={1800} height={1200} className="mx-auto rounded-2xl object-cover h-full w-full object-center" draggable={false} loading="lazy"/>
  </ContainerScroll><p className="scroll-credit">Illustrative stock photography / Unsplash. Research prototype.</p>
 </section>;
}

# PulseCast design refinement

Skill: design-taste-frontend. Mode: redesign preserving content and behavior.

Reading: a clinical research experience for clinicians, participants, and hackathon judges. Native CSS with an Apple-inspired aesthetic, not an official Apple design system.

Dials: DESIGN_VARIANCE 6, MOTION_INTENSITY 4, VISUAL_DENSITY 3 on the landing surfaces. The actual research dashboard retains its data-oriented layout and semantic chart colors; it is outside this marketing-page skill's scope.

## Existing identity and flow

- Blue accent #0071e3, system sans typography, white-on-blue medical cross wordmark.
- Overview, Cohort, Validation, Methodology navigation. The labels change appropriately in patient view.
- home and workspace anchors, assigned patient 004, replay, signal confidence gating, assistant, downloads, evidence dialog, and persistent theme toggle.
- GitHub Pages repository subpath and Render backend URL remain intact.
- Existing metadata and title preserved, apart from replacing the title separator.

## Retire

- A two-row 110px floating glass navigation on desktop.
- Centered billboard copy, decorative eyebrow dots, and fake hero signal readout.
- Repeated numbered labels and duplicate marketing CTAs.
- Decorative orbital signal universe and a dark inverted feature card inside light mode.
- Remote Google font imports and tiny decorative metadata.

## Refine

- One-line desktop navigation under 80px, solid themed surfaces, responsive two-row mobile navigation.
- Split hero with natural headline, separate 4K video panel, and one primary action.
- Full theme consistency; the photograph/video retains natural colors but no inverted text sections.
- Cohesive 18px containers, 10px controls, and 999px primary buttons.
- Original AI-generated physiology image explicitly identified as illustrative.
- Existing consultation image retained, with credit outside the photograph.
- Tabler icons from the official SVG library, preserving the custom brand cross.
- IntersectionObserver reveals explain content hierarchy; continuous video respects reduced motion and data-saving preferences.

## Verification

Build, cohort tests, mobile overflow, desktop navigation geometry, light/dark states, patient scope, artifact suppression, evidence dialog, export, live assistant status, and deployment checks.

## Completed checks

- Vite production build, both cohort/replay tests, diff whitespace check, and dependency audit pass (zero production vulnerabilities).
- Browser inspection at 1470px desktop and 390px mobile: no horizontal overflow, video playing, SVG icons rendered, both themes readable, patient cohort selector absent, evidence dialog opens.
- Production-preview Lighthouse: Performance 100, Accessibility 100, SEO 100. Best Practices 73 reflects the preview origin being excluded by backend CORS and cookies on third-party Pexels imagery. This is a local audit, not a production speed guarantee.
- Landing preflight: split hero, varied editorial layout, preserved identity/navigation, labeled illustrative media, native typography, single icon family, consistent theme surfaces, reduced-motion/data-saving fallback, and primary/secondary actions checked. Dashboard cards retain their functional data hierarchy.

## Cinematic reference update

User requested Remix.run's majestic presentation. Applied its scale and kinetic-landscape direction through an original cyan PulseCast wordmark, canvas physiology field, subtle existing laboratory video, and stronger editorial typography. Centered composition follows the user's explicit visual reference. Cross logo, full-width workspace, themes, patient/doctor controls, assistant, timeline, search, and research limitations remain intact. No Remix artwork or code was copied. Canvas animation is viewport-gated and reduced-motion aware. Mobile at 390px has no horizontal overflow; both themes were visually checked.

## Focused medical homepage and subpages

User clarified that the Remix composition should use a medical background. The homepage now shows a full-screen continuous laboratory film with prominent lettering and centered editorial content; dashboard information is on hash-addressable Overview, Cohort, Validation and Methodology pages. Hash routes support reloads and browser back/forward on GitHub Pages. Accordion deep links open Methodology with the selected explanation. Existing stock video is credited and reduced-motion/data-saving visitors see its poster. Patient view switching retains presentation-only scope.

## Scroll-controlled dot scene

Replaced ambient-only motion with a pinned four-chapter scene: scroll progress drives original 3D heart point-cloud rotation, camera framing, laboratory zoom, wordmark departure, and chapter fades. The dots form a stylized heart rather than a diagnostic anatomical model. Links enter existing research subpages. Reduced-motion visitors get static stacked chapters. Invisible chapters are removed from keyboard navigation and marked aria-hidden. Scrolling and scene transitions were inspected in-browser.

## Dissolve and reassembly particles

Replaced the CPU dot surface with a WebGL morph system. Desktop uses 200,000 particles and mobile 60,000; these are real rendering budgets, not a claim of billions. Scroll drives heart → DNA helix → abstract ribbon → heart, with turbulent dispersal between targets and cyan/gold/pink/green color evolution. Buffers are uploaded once; the GPU interpolates position, perspective, additive glow and color. Scene visibility and reduced-motion support remain. WebGL-unavailable clients keep a medical-footage fallback. This is original generative artwork, not a copy of the reference asset.

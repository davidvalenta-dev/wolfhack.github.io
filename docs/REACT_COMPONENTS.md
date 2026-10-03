# React component integration

This existing Vite application now supports React 19, TypeScript, Tailwind 4, and the shadcn project structure. Components live at `/components/ui`; styles live at `src/styles` and the user menu's local CSS module. The `@/components/ui` alias maps to the repository folder, and `components.json` tells the shadcn CLI where to place future UI components. Keeping reusable components here avoids mixing their implementation with the existing dashboard orchestration.

Run `npm install`, `npm run dev`, and `npm run build`. The build checks TypeScript. To add a shadcn component, run `npx shadcn@latest add button`. An existing configuration is provided, so initialization is not required. For a new project, use `npx shadcn@latest init`, install TypeScript/React types and Tailwind's Vite plugin, then configure the alias and stylesheet as demonstrated here.

- `container-scroll-animation.tsx`: supplied scroll progress, perspective, rotation, responsive scale and header translation, with typed props and reduced-motion support.
- `hero-scroll-demo.tsx`: Vite-compatible demo with a normal image instead of `next/image`, medical Unsplash photography, and PulseCast copy. The sample's extra 1500px padding is omitted for a usable page.
- `user-menu.tsx`: supplied menu, keyboard navigation, animated highlight, theme selection, desktop portal and mobile sheet. Its referenced CSS module was absent from the attachment; a complete theme-aware module is supplied here.
- `user-menu-demo.tsx`: connected to real research navigation, existing export, and appearance preferences. Reset demo replaces sign out because this prototype has no authentication session. No billing or fictional account actions are added.
- `src/react/mount.tsx`: retained React roots coexist with the existing vanilla dashboard and its frequent replay renders. No context providers are required.

Tailwind preflight is intentionally omitted to preserve existing chart/dashboard styles. Theme utility tokens map onto PulseCast variables; the supplied palette is adapted rather than overwriting the existing global surfaces. Both `motion` and `framer-motion` are installed as requested, with Lucide icons for the new menu and the existing medical cross retained.

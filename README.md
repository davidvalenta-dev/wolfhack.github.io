# WolfHacks26
## PulseCast

The frontend combines an original Apple-inspired editorial design with a clinical research workspace, Doctor and Patient demo views, synchronized physiological charts, and a hosted Gemini assistant. The supplied Python/Databricks agent is also retained. See [backend/INTEGRATION.md](backend/INTEGRATION.md) for setup and hosting. Patient view is a presentation demo fixed to participant 004, not authenticated access control. The backend must be deployed and configured separately for live LLM answers.

Frontend research explorer for wearable-based metabolic phenotype similarity.

### Run locally

```sh
npm install
npm run dev
```

`npm test` checks cohort labels and replay boundaries. `npm run build` creates the production site.

### Data and model status

The app includes actual HbA1c labels from [PhysioNet BIG IDEAs v1.1.3](https://physionet.org/content/big-ideas-glycemic-wearable/1.1.3/). The source demographics are in `data/raw/physionet-demographics.csv`. Wearable values, quality, feature differences, and similarity scores are synthetic demonstration fixtures in `src/data/cohort.js`. A trained classifier, measured accuracy, and CGM validation are not implemented. Gemini generates explanations from the same synthetic demo context through a separately hosted Render backend; the API key stays on the server. The UI labels these boundaries explicitly.

The latest direction supersedes the earlier near-term glucose-rise proposal: predict cohort similarity from wearable-only features, use HbA1c as labels, and reserve CGM for independent validation. Fit all preprocessing within participant-held-out folds. See the app's Methodology view for the integration plan.

### Publishing

The Pages workflow builds and deploys pushes to `main`. Site: https://davidvalenta-dev.github.io/wolfhack.github.io/

See [SPECS.md](SPECS.md) for the project context, references, candidate directions, technical requirements, and communication plan.

See [PROJECT_OUTLINE.md](PROJECT_OUTLINE.md) for the current PulseCast concept and demo structure.

See [REPO_OUTLINE.md](REPO_OUTLINE.md) for the repository map, frontend flow, data contract, implementation stages, and scope guardrails.

### Presentation experience

- Continuous 4K laboratory stock film on desktop, HD footage on mobile/data-saving connections, and a still poster for reduced-motion preferences. Film and stock imagery: Kindel Media and Mikhail Nilov / Pexels. Bottom consultation photograph: cottonbro studio / Pexels. Media is illustrative and does not depict research participants.
- Persistent light/dark appearance, floating navigation, and a responsive medical dashboard.
- Three guided replay scenes: clean baseline, motion artifact, and recovery. Scores and chart segments are suppressed for low-quality synthetic windows.
- Current-window comparisons with the synthetic session baseline, an inspectable confidence ring, and a quality timeline.
- Downloadable JSON session brief including provenance and research limitations, and an accessible evidence dialog.
- Public research data only. The patient view switch is not authentication.

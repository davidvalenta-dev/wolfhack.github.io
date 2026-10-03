# Deploy the demo agent on Render

1. Open https://render.com/deploy?repo=https://github.com/davidvalenta-dev/wolfhack.github.io and sign in.
2. Review the `pulsecast-agent` Blueprint. It explicitly selects the **free** plan.
3. Add your Gemini API key as `GEMINI_API_KEY` in Render's secret environment variable field. Create a key at https://aistudio.google.com/apikey. Do not paste it into chat, commit it, or put it in frontend variables.
4. Confirm `GEMINI_MODEL` is a model available on your account's free tier; change it in Render if necessary.
5. Deploy. Open the service's `/health` URL to confirm `llm_configured: true`.
6. Set the GitHub Actions repository variable `PULSECAST_API_URL` to the service's HTTPS URL, then rerun the Pages workflow. The assistant will call the Render service.

The Render service uses the supplied agent orchestration with a Gemini client and public-demo tools. It needs no Databricks account and no large training dependencies. Its tool data matches the frontend's synthetic replay and actual public HbA1c labels; it does not claim trained predictions or measured glucose validation. The original Databricks backend remains available in `service/api.py`.

Free services can sleep. The frontend allows extra time for a cold start. Gemini free-tier access is model/account dependent. A per-process request throttle limits casual demo usage; real authentication and deployment-wide rate limiting are required before using private data or paid keys.

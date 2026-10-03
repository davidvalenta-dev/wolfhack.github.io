/** Connect the supplied FastAPI/Databricks agent without exposing server credentials. */
const api=import.meta.env.VITE_API_URL || (location.hostname==='localhost'?'/api':'');
export async function askAgent({subject_id,question,audience,minute=32}){
 if(!api)throw new Error('The live LLM is not connected on this hosted demo. Configure VITE_API_URL with your deployed backend URL.');
 const response=await fetch(`${api.replace(/\/$/,'')}/agent`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({subject_id,question,audience,minute,max_steps:3}),signal:AbortSignal.timeout(120000)});
 if(!response.ok)throw new Error(`Agent service unavailable (${response.status}). Check server credentials and processed data artifacts.`);
 const result=await response.json();if(typeof result.answer!=='string')throw new Error('Agent returned an invalid response.');return result;
}

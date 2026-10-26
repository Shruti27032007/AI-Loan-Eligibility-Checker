const $ = id => document.getElementById(id);
const money = n => "₹" + Number(n).toLocaleString("en-IN", {maximumFractionDigits: 2});

async function post(url, data){
  const r = await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
  return await r.json();
}
function show(id, html, cls=""){
  const el=$(id); el.className="result "+cls; el.innerHTML=html;
}
function userData(){
  return {
    income:$("income").value, age:$("age").value, credit_score:$("credit").value,
    employment:$("employment").value, loan_amount:$("loan").value, tenure:$("tenure").value
  };
}
async function checkEligibility(){
  const d=await post("/api/eligibility",userData());
  show("eligibilityResult",
    `<strong>${d.eligible ? "✓ Demo Eligible" : "△ Demo Review Needed"}</strong>
     <br>Model score: <b>${d.score}/100</b>
     <ul>${d.reasons.map(x=>`<li>${x}</li>`).join("")}</ul>
     <small>${d.disclaimer}</small>`,
     d.eligible?"success":"warning");
}
async function calculateEMI(){
  const d=await post("/api/emi",{principal:$("emiPrincipal").value,rate:$("emiRate").value,years:$("emiYears").value});
  show("emiResult",`<b>Monthly EMI:</b> ${money(d.emi)}<br><b>Total interest:</b> ${money(d.interest)}<br><b>Total payment:</b> ${money(d.total)}`,"success");
}
async function analyzeCredit(){
  const d=await post("/api/credit",{credit_score:$("creditOnly").value});
  show("creditResult",`<b>${d.level}</b><ul>${d.tips.map(x=>`<li>${x}</li>`).join("")}</ul>`);
}
async function getAITips(){
  const d=await post("/api/ai-tips",userData());
  show("aiResult",`<b>${d.source.toUpperCase()}</b><br>${(d.message||"").replace(/\n/g,"<br>")}`);
}
async function saveRecord(){
  const d=await post("/api/save",userData());
  show("saveResult",d.saved ? "✓ Record sent to Google Sheets." : `Not saved: ${d.message || "Configure GOOGLE_SHEETS_WEBHOOK_URL first."}`);
}

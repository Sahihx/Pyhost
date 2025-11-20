document.getElementById("codeForm").addEventListener("submit", async (e)=>{
    e.preventDefault();
    let code = e.target.code.value;
    let res = await fetch("/run", {method:"POST", body: new URLSearchParams({code})});
    let data = await res.json();
    if(data.job_id){
        addJob(data.job_id);
        e.target.code.value = "";
    }
});

function addJob(job_id){
    let ul = document.getElementById("jobsList");
    let li = document.createElement("li");
    li.dataset.jobId = job_id;
    li.innerHTML = `Job ${job_id} - <span class="status">running</span> <button class="stopBtn">Stop</button><pre class="log"></pre>`;
    ul.appendChild(li);
    li.querySelector(".stopBtn").addEventListener("click", ()=>stopJob(job_id, li));
}

async function stopJob(job_id, li){
    await fetch("/stop", {method:"POST", body:new URLSearchParams({job_id})});
    li.querySelector(".status").textContent = "stopped";
}

async function updateLogs(){
    document.querySelectorAll("#jobsList li").forEach(async li=>{
        let job_id = li.dataset.jobId;
        let res = await fetch(`/status/${job_id}`);
        let data = await res.json();
        li.querySelector(".status").textContent = data.status;
        li.querySelector(".log").textContent = data.log;
    });
}

setInterval(updateLogs, 2000);

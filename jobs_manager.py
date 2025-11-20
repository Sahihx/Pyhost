import subprocess, threading, psutil, json, os

DB_FILE = "jobs_db.json"

class JobManager:
    def __init__(self):
        self.jobs = {}  # job_id: {"process": proc, "status": str, "log": str}
        self.load_jobs()
        self.job_counter = max([int(k) for k in self.jobs.keys()] + [0]) + 1

    def save_jobs(self):
        data = {str(k): {"status": v["status"], "log": v["log"]} for k,v in self.jobs.items()}
        with open(DB_FILE, "w") as f:
            json.dump(data, f)

    def load_jobs(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                self.jobs = json.load(f)
        else:
            self.jobs = {}

    def start_job(self, code):
        job_id = self.job_counter
        self.job_counter += 1
        filename = f"job_{job_id}.py"
        with open(filename, "w") as f:
            f.write(code)

        proc = subprocess.Popen(["python", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.jobs[str(job_id)] = {"process": proc, "status": "running", "log": ""}
        
        threading.Thread(target=self._capture_output, args=(str(job_id),), daemon=True).start()
        threading.Thread(target=self._monitor_resources, args=(str(job_id),), daemon=True).start()
        self.save_jobs()
        return job_id

    def _capture_output(self, job_id):
        proc = self.jobs[job_id]["process"]
        for line in proc.stdout:
            self.jobs[job_id]["log"] += line
        self.jobs[job_id]["status"] = "finished"
        self.save_jobs()

    def _monitor_resources(self, job_id):
        proc = self.jobs[job_id]["process"]
        try:
            p = psutil.Process(proc.pid)
            while proc.poll() is None:
                cpu = p.cpu_percent(interval=1)
                mem = p.memory_info().rss / (1024*1024)
                if cpu > 80 or mem > 100:
                    proc.terminate()
                    self.jobs[job_id]["status"] = "terminated"
                    self.jobs[job_id]["log"] += "\n[Terminated: Resource limit exceeded]"
                    self.save_jobs()
                    break
        except:
            pass

    def stop_job(self, job_id):
        job_id = str(job_id)
        if job_id in self.jobs:
            proc = self.jobs[job_id]["process"]
            proc.terminate()
            self.jobs[job_id]["status"] = "stopped"
            self.save_jobs()
            return True
        return False

    def get_status(self, job_id):
        job_id = str(job_id)
        job = self.jobs.get(job_id, None)
        if job:
            return {"status": job["status"], "log": job["log"]}
        return {"status": "unknown", "log": ""}

    def list_jobs(self):
        return {k: {"status": v["status"]} for k, v in self.jobs.items()}
      

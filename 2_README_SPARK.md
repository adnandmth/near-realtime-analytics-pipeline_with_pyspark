# ✅ Step-by-Step Health Checks for Spark Cluster

This guide helps you verify that your Spark master and worker nodes are running and can execute jobs.

---

## 1. Check Spark Containers Are Running

```sh
docker ps | grep spark
```
You should see containers like `spark-master`, `spark-worker-1`, `spark-worker-2`, etc.

---

## 2. Check Spark Master Web UI

Open your browser and go to:  
[http://localhost:8080](http://localhost:8080)  
(or use the port mapped in your `docker-compose.yml`)

You should see the Spark Master UI, listing all connected workers.

---

## 3. Check Spark Worker Web UI

Each worker usually exposes a web UI at ports like 8081, 8082, etc.  
Example: [http://localhost:8081](http://localhost:8081)

---

## 4. Check Worker Registration

On the Spark Master UI, you should see all workers listed as **ALIVE** with their resources (cores, memory).

---

## 5. Check Spark Master Logs

```sh
docker logs spark-master | tail -n 50
```
Look for lines like:
```
Registering worker
Successfully registered worker
```
and no error messages.

---

## 6. Check Spark Worker Logs

```sh
docker logs spark-worker-1 | tail -n 50
```
Look for successful registration and no errors.

---

## 7. Submit a Test Spark Job

You can run a simple Spark Pi job to test cluster functionality:

```sh
docker exec -it spark-master-1 spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --class org.apache.spark.examples.SparkPi \
  /opt/bitnami/spark/app/jobs/pipeline_1_job.py
```

You should see output with `Pi is roughly ...` if the job runs successfully.

---

## 8. Check Job Status in Web UI

While the job is running, refresh the Spark Master UI.  
You should see the job listed under "Running Applications" or "Completed Applications".

---

## 9. (Optional) Submit a Python Job

If you want to test PySpark:

```sh
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  /opt/bitnami/spark/examples/src/main/python/pi.py 10
```

---

## ✅ Summary Table

| Component      | Check             | Expected Output         |
| -------------- | ----------------- | ---------------------- |
| Spark Master   | Web UI            | Shows all workers      |
| Spark Workers  | Web UI            | Status: ALIVE          |
| Master/Worker  | Logs              | No errors              |
| Job Submission | Run example job   | Pi result, no errors   |

---

## 📚 References

- [Bitnami Spark Docs](https://github.com/bitnami/containers/tree/main/bitnami/spark)
- [Apache Spark Official Docs](https://spark.apache.org/docs/latest/)
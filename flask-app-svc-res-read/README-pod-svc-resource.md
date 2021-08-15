Running Flask APP Local Virtual Environment

## set environmental variable

set APP_VERSION=V1
echo %APP_VERSION%
V1

Start APP

python myapp.py
App Version V1

- Serving Flask app "myapp" (lazy loading)
- Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
- Debug mode: on
- Restarting with stat
  App Version V1 >>>>> Note V1
- Debugger is active!
- Debugger PIN: 228-535-651
- Running on http://0.0.0.0:9999/ (Press CTRL+C to quit)

---

## Build Docker Image and Upload to docker hub

docker build -t ajaysinghdocker/flask-app .

TEST NEW IMAGE LOCALLY
docker run -d -p 9999:9999 ajaysinghdocker/flask-app

curl http://localhost:9999/info
App Version V2

## push image to docker hub

docker push ajaysinghdocker/flask-app

#------------------------------------------------------------

# Deploy in Kubernetes Cluster - Docker for Desktop

kubectl apply -f pod-svc-resource.yml
pod/flaskapi-pod1 created
service/flask-service unchanged

#### kubectl get pods

NAME READY STATUS RESTARTS AGE
flaskapi-pod1 1/1 Running 0 4m19s

#### kubectl get svc

NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE
flask-service LoadBalancer 10.110.179.222 localhost 9999:32485/TCP 22s

## Check StartUp log for Flask APP Since pod has one container we are not listing

pod1 log
$ winpty -Xallow-non-tty kubectl logs flaskapi-pod1 | grep -i version
App Version V1

# Container Log

$ winpty -Xallow-non-tty kubectl logs flaskapi-pod1 | grep -i version
App Version V1
192.168.65.3 - - [15/Aug/2021 19:08:57] "GET /version HTTP/1.1" 200 -
192.168.65.3 - - [15/Aug/2021 19:09:06] "GET /version HTTP/1.1" 200 -

# Now since we used load balancer type

Using version End Point in browser if u keep refreshing it will alternate between Blue and Green
http://127.0.0.1:9999/version

# check APP info

$ curl -s http://localhost:9999/info
App Version V1

# Now Add another Service NodePort and see if you can reachj ur app

---

apiVersion: v1
kind: Service
metadata:
name: flask-service-node-port
spec:
ports:

- port: 80
  protocol: TCP
  targetPort: 9999
  selector:
  app: flaskapi
  type: NodePort

$ kubectl get svc
NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE
flask-service LoadBalancer 10.110.179.222 localhost 9999:32485/TCP 16h
flask-service-node-port NodePort 10.98.204.243 <none> 80:30414/TCP 2m

# Now we will ue node port to get same info

curl -s http://localhost:30414/info
App Version V1

### check how much memory and cpu pod is consuming

$ kubectl top pod
W0815 14:34:25.633179 38852 top_pod.go:140] Using json format to get metrics. Next release will switch to protocol-buffers, switch early by passing --use-protocol-buffers flag
NAME CPU(cores) MEMORY(bytes)
flaskapi-pod1 5m 37Mi

### change limits and reuest to 10Mi of memory and see effect

spec:
containers:

- name: flaskapi
  image: ajaysinghdocker/flask-app
  imagePullPolicy: Always
  resources:
  limits:
  cpu: 10m
  memory: 10Mi
  requests:
  cpu: 5m
  memory: 10Mi

### delete and recreate

kubectl delete -f pod-svc-resource.yml
pod "flaskapi-pod1" deleted
service "flask-service" deleted
service "flask-service-node-port" deleted

$ kubectl get pods
NAME READY STATUS RESTARTS AGE
flaskapi-pod1 0/1 OOMKilled 2 2m32s

Out of Memory Killed

$ kubectl get events
LAST SEEN TYPE REASON OBJECT MESSAGE
2m18s Warning SystemOOM node/docker-desktop System OOM encountered, victim process: python, pid: 94965
97s Warning SystemOOM node/docker-desktop System OOM encountered, victim process: python, pid: 97608
42s Warning SystemOOM node/docker-desktop System OOM encountered, victim process: python, pid: 2107
57m Normal Killing pod/flaskapi-pod1 Stopping container flaskapi
36m Normal Scheduled pod/flaskapi-pod1 Successfully assigned default/flaskapi-pod1 to docker-desktop
35m Normal Pulling pod/flaskapi-pod1 Pulling image "ajaysinghdocker/flask-app"

SInce Pod is not actively running

$ kubectl top pods
W0815 14:43:37.245477 24196 top_pod.go:140] Using json format to get metrics. Next release will switch to protocol-buffers, switch early by passing --use-protocol-buffers flag
NAME CPU(cores) MEMORY(bytes)
flaskapi-pod1 0m 0Mi

Change Back Memory Limit to 100Mi and This time make it CPU limit very low 1m

resources:
limits:
cpu: 1m
memory: 100Mi
requests:
cpu: 1m
memory: 100Mi

Metric server CPU is over commited 11m than limit stil APP is functioning

$ kubectl top pods
W0815 14:51:34.184527 12532 top_pod.go:140] Using json format to get metrics. Next release will switch to protocol-buffers, switch early by passing --use-protocol-buffers flag
NAME CPU(cores) MEMORY(bytes)
flaskapi-pod1 11m 15Mi

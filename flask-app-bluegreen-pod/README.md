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

Build Docker Image

docker build -t myapp .

# Deploy in Kubernetes Cluster - Docker for Desktop

kubectl apply -f flaskapp-multi-pod.yml  
pod/flaskapi-pod1 created
pod/flaskapi-pod2 created
service/flask-service created

#### kubectl get pods

NAME READY STATUS RESTARTS AGE
flaskapi-pod1 1/1 Running 0 18s
flaskapi-pod2 1/1 Running 0 18s

#### kubectl get svc

NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE
flask-service LoadBalancer 10.110.179.222 localhost 9999:32485/TCP 22s

## Check StartUp log for Flask APP in both pods . Since pod has one container we are not listing

pod1 log
$ winpty -Xallow-non-tty kubectl logs flaskapi-pod1 | grep -i version
App Version V1

Pod2 log
$ winpty -Xallow-non-tty kubectl logs flaskapi-pod2 | grep -i version
App Version V2

# Now since we used load balancer type

App version will change between v2 and v2

Using info End Point and curl command

$ curl -s http://localhost:9999/info
App Version V2

$ curl -s http://localhost:9999/info
App Version V2

$ curl -s http://localhost:9999/info
App Version V1

Using version End Point in browser if u keep refreshing it will alternate between Blue and Green
http://127.0.0.1:9999/version

https://www.educative.io/courses/practical-guide-to-kubernetes/JQ9PV6YPgQl

Allocating Excessive Memory more than available on nodes

$ kubectl top nodes
W0815 15:03:08.336755 21648 top_node.go:119] Using json format to get metrics. Next release will switch to protocol-buffers, switch early by passing --use-protocol-buffers flag
NAME CPU(cores) CPU% MEMORY(bytes) MEMORY%
docker-desktop 467m 23% 1220Mi 64%

    resources:
      limits:
        cpu: 1m
        memory: 6000Mi
      requests:
        cpu: 1m
        memory: 2000Mi

This time, the status of the Pod is Pending. Kubernetes could not place it anywhere in the cluster and is waiting until the situation changes.

Even though memory requests are associated with containers, it often makes sense to translate them into Pod requirements. We can say that the requested memory of a Pod is the sum of the requests of all the containers that form it. In our case, the Pod has only one container, so the requested memory for the Pod and the container are equal. The same can be said for limits.

During the scheduling process, Kubernetes sums the requests of a Pod and looks for a node that has enough available memory and CPU. If Pod’s request cannot be satisfied, it is placed in the pending state in the hope that resources will be freed on one of the nodes, or that a new server will be added to the cluster.

C:\Users\ajay\_\python\flask\kube-python-app\flask-app-svc-res-read>kubectl apply -f pod-svc-resource-over-node-memory.yml
pod/flaskapi-pod1 created
service/flask-service unchanged
service/flask-service-node-port unchanged

C:\Users\ajay\_\python\flask\kube-python-app\flask-app-svc-res-read>kubectl get pods
NAME READY STATUS RESTARTS AGE
flaskapi-pod1 0/1 Pending 0 4s

$ kubectl get events | tail -5
59s Warning FailedScheduling pod/flaskapi-pod1 0/1 nodes are available: 1 Insufficient memory.
37s Warning FailedScheduling pod/flaskapi-pod1 0/1 nodes are available: 1 Insufficient memory.

C:\Users\ajay\_\python\flask\kube-python-app\flask-app-svc-res-read>kubectl describe pod flaskapi-pod1
Name: flaskapi-pod1
Namespace: default
Priority: 0
Node: <none>
Labels: app=flaskapi
version=v1
Annotations: <none>
Status: Pending
IP:
IPs: <none>
Containers:
flaskapi:
Image: ajaysinghdocker/flask-app
Port: 9999/TCP
Host Port: 0/TCP
Limits:
cpu: 1m
memory: 6000Mi
Requests:
cpu: 1m
memory: 2000Mi
Environment:
APP_VERSION: V1
Mounts:
/var/run/secrets/kubernetes.io/serviceaccount from default-token-sjmxx (ro)
Conditions:
Type Status
PodScheduled False
Volumes:
default-token-sjmxx:
Type: Secret (a volume populated by a Secret)
SecretName: default-token-sjmxx
Optional: false
QoS Class: Burstable
Node-Selectors: <none>
Tolerations: node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
Type Reason Age From Message

---

Warning FailedScheduling 5m28s default-scheduler 0/1 nodes are available: 1 Insufficient memory.
Warning FailedScheduling 5m28s default-scheduler 0/1 nodes are available: 1 Insufficient memory.

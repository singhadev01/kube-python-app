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

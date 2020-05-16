# Scheduler
```shell
$ vim scheduler.sh
#!/bin/bash

SERVER='localhost:8080'

while true;
do
    for PODNAME in $(kubectl --server $SERVER get pods --all-namespaces -o json | jq '.items[] | select(.spec.schedulerName == "my-scheduler") | select(.spec.nodeName == null) | .metadata.name' | tr -d '"');
    do
	    NAMESPACES=($(kubectl --server $SERVER get pods --all-namespaces -o json | jq '.items[] | select(.spec.schedulerName == "my-scheduler") | select(.metadata.name == "'$PODNAME'") | .metadata.namespace' | tr -d '"'))
	    NODES=($(kubectl --server $SERVER get nodes -o json | jq '.items[].metadata.name' | tr -d '"'))
	    NUMNODES=${#NODES[@]}
        CHOSEN=${NODES[$[$RANDOM % $NUMNODES]]}
	    curl --header "Content-Type:application/json" --request POST --data '{"apiVersion":"v1", "kind": "Binding", "metadata": {"name": "'$PODNAME'"}, "target": {"apiVersion": "v1", "kind": "Node", "name": "'$CHOSEN'"}}' http://$SERVER/api/v1/namespaces/$NAMESPACES/pods/$PODNAME/binding/
        echo "Assigned $PODNAME to $CHOSEN in NAMESPACES:$NAMESPACES"
    done
    sleep 1
done
```
## Run Scheduler
```shell
$ chmod +x scheduler.sh
$ ./scheduler.sh
```
## Run Pod
```yaml
$ vim sc-test-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx

spec:
  schedulerName: my-scheduler
  containers:
  - name: nginx
    image: nginx:1.10

$ kubectl apply -f sc-test-pod.yaml
```
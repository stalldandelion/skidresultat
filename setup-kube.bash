#/bin/bash
minikube start --driver=docker
minikube addons enable registry
eval $(minikube docker-env)
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml

until ! kubectl get pods --namespace tekton-pipelines | grep "0/1"
do
        echo "Wating for tekton pods to go up...."
        sleep 5
done

sleep 10
kubectl apply -f tekton/pipelineresources/skidresultat-gitresource.yaml
kubectl apply -f tekton/pipelineresources/skidresultat-imageresource.yaml
kubectl apply -f tekton/pipelines/skidresultat-pipeline.yaml
kubectl apply -f tekton/tasks/s2i-build-push.yaml
tkn pipeline start skidresultat-pipeline --resource skidresultat-git=skidresultat-git-res --resource skidresultat-image=skidresultat-image-res
tkn pipeline logs --last -f
kubectl apply -f kubernetes/deployment/dc.yaml
kubectl port-forward $(kubectl get pod --selector=app=skidresultat -o name) 8080:8080
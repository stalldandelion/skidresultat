# Kubernetes
## Installera minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube

# Docker
## Installera docker-desktop (Mac)
https://desktop.docker.com/mac/stable/amd64/Docker.dmg

# Kubernetes
## Starta kubernetes
minikube start --driver=docker
minikube addons enable registry
eval $(minikube docker-env)

# Tekton
## installera
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml

## Installera pipeline
git checkout https://github.com/stalldandelion/skidresultat.git
cd skidresultat
kubectl apply -f tekton/pipelineresources/skidresultat-gitresource.yaml 
kubectl apply -f tekton/pipelineresources/skidresultat-imageresource.yaml
kubectl apply -f tekton/pipelines/skidresultat-pipeline.yaml
kubectl apply -f tekton/tasks/s2i-build-push.yaml
tkn pipeline start skidresultat-pipeline --resource skidresultat-git=skidresultat-git-res --resource skidresultat-image=skidresultat-image-res

kubectl run -i -t skidresultat --image=localhost:5000/misu/skidresultat
kubectl port-forward pod/skidresultat 8080:8080

## Kör applikationen i terminal
git checkout https://github.com/stalldandelion/skidresultat.git
cd skidresultat
pip install -r requirements.txt

python ./skidresultat-app.py
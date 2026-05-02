# tierdemo-deploy (deprecated)

Workload manifests were **moved back** into [`gitops-inception-agribora`](https://github.com/omondijeff/gitops-inception-agribora) under `apps/` (**Option A**: one GitOps repo for platform + K8s YAML).

Application **source code** and the container build live in [`tierdemo-app`](https://github.com/omondijeff/tierdemo-app) (image `ghcr.io/omondijeff/tierdemo-app`).

You can **delete this GitHub repository** when no longer needed; Argo CD should not reference it after `gitops-inception-agribora` `argocd/config/app-git-source.yaml` points at the GitOps repo (default again).

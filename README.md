# tierdemo-deploy

Kubernetes manifests for the **three-tier demo** (Flask **frontend**, **PostgreSQL**, **Redis**): Kustomize **bases**, **local** overlays with **NetworkPolicies**, and **ExternalSecrets** wired to HashiCorp Vault.

The **GitOps / platform** repository ([`gitops-inception-agribora`](https://github.com/omondijeff/gitops-inception-agribora)) installs Flux, Argo CD, Traefik, Vault, etc. Argo CD **Applications** point **here** for `database`, `redis`, and `frontend` (`apps/overlays/local/<component>`).

## Layout

| Path | Purpose |
|------|---------|
| `apps/base/<component>/` | Namespace, Deployments, Services, `IngressRoute` (frontend), ESO resources |
| `apps/overlays/local/<component>/` | Base + network policies for local / dev clusters |
| `apps/network-policies/` | Shared policy fragments |

## Publish this repository

Create an empty GitHub repository (for example **`tierdemo-deploy`** under your user or org), then:

```bash
cd /path/to/tierdemo-deploy
git init
git branch -M main
git add .
git commit -m "chore: initial three-tier deploy manifests"
git remote add origin https://github.com/<you>/tierdemo-deploy.git
git push -u origin main
```

Ensure [`gitops-inception-agribora`](https://github.com/omondijeff/gitops-inception-agribora) **`argocd/config/app-git-source.yaml`** uses the same **`repoURL`** and branch as this remote (defaults target **`main`**).

If the repo is **private**, register credentials in the cluster (see `gitops-inception-agribora/scripts/argocd-register-github-repo.sh` with `REPO_URL` matching this repository).

## Validate locally

```bash
kubectl kustomize apps/overlays/local/frontend   | head
kubectl kustomize apps/overlays/local/database   | head
kubectl kustomize apps/overlays/local/redis      | head
```

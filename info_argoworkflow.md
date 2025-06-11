---

## ✅ Updated Plan (with ArgoCD CLI)

### **🔁 Flow Overview**

1. Jenkins sends chart name + version to Argo Workflows.
2. Argo Workflow creates and syncs ArgoCD `Application` using **`argocd` CLI**.
3. Chart A is deployed → waits for sync to complete → Chart B is deployed.

---

## 🧩 Argo Workflow YAML (Using `argocd` CLI)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: deploy-helm-charts-
spec:
  entrypoint: deploy-charts
  arguments:
    parameters:
    - name: chartAName
    - name: chartAVersion
    - name: chartBName
    - name: chartBVersion

  templates:
  - name: deploy-charts
    steps:
    - - name: deploy-chart-a
        template: deploy-to-argocd
        arguments:
          parameters:
          - name: chartName
            value: "{{workflow.parameters.chartAName}}"
          - name: chartVersion
            value: "{{workflow.parameters.chartAVersion}}"
    - - name: deploy-chart-b
        template: deploy-to-argocd
        arguments:
          parameters:
          - name: chartName
            value: "{{workflow.parameters.chartBName}}"
          - name: chartVersion
            value: "{{workflow.parameters.chartBVersion}}"

  - name: deploy-to-argocd
    inputs:
      parameters:
      - name: chartName
      - name: chartVersion
    container:
      image: argoproj/argocd:v2.11.0  # Use latest stable
      command: [sh, -c]
      args:
        - |
          echo "Deploying chart: {{inputs.parameters.chartName}}:{{inputs.parameters.chartVersion}}"

          argocd login argocd-server.argocd.svc.cluster.local:443 \
            --username admin \
            --password $ARGOCD_PASSWORD \
            --insecure

          argocd app create {{inputs.parameters.chartName}} \
            --repo https://your-helm-repo.example.com \
            --helm-chart {{inputs.parameters.chartName}} \
            --revision {{inputs.parameters.chartVersion}} \
            --dest-server https://kubernetes.default.svc \
            --dest-namespace default \
            --project default \
            --sync-policy automated

          echo "Waiting for sync to complete..."
          argocd app wait {{inputs.parameters.chartName}} --health --operation
    env:
    - name: ARGOCD_PASSWORD
      valueFrom:
        secretKeyRef:
          name: argocd-secret
          key: admin.password
```

---

## 🔐 Prerequisites

1. **ArgoCD CLI image**: Use `argoproj/argocd` container image.
2. **Authentication**:

   * Either use admin credentials (mounted as env var)
   * Or use a token stored in a secret (recommended).
3. **Helm repo must be configured in ArgoCD** or use `--repo` to point to it directly.

---

## 🧪 Jenkins Step

```bash
argo submit --serviceaccount argo \
  --parameter chartAName=my-app-a \
  --parameter chartAVersion=1.2.3 \
  --parameter chartBName=my-app-b \
  --parameter chartBVersion=4.5.6 \
  --watch deploy-helm-on-argocd.yaml
```

---

## ✅ Notes

* You can add `argocd app sync` if you're updating existing apps.
* Optionally use `argocd app set` to change versions if app already exists.

---

Would you like me to also generate the Jenkinsfile and Secret manifest (`argocd-secret`) used above?

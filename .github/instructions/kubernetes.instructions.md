---
applyTo: "**/*.yaml,**/*.yml,**/*.json"
---
# Buenas Prácticas de Kubernetes

## 1. **Configuración de Pods y Deployments**

### 1.1 Especificación de Recursos
- **SIEMPRE** especifica límites y requests de recursos
- Usa requests para garantizar recursos mínimos
- Usa limits para evitar que un pod consuma todos los recursos

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web-app
    version: v1.2.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
        version: v1.2.0
    spec:
      containers:
      - name: web-app
        image: myorg/web-app:v1.2.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        # ✅ Health checks obligatorios
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 1.2 Labels y Selectors
- Usa labels consistentes y descriptivos
- Incluye información de versión, entorno y aplicación
- Usa recommended labels de Kubernetes

```yaml
metadata:
  labels:
    # ✅ Recommended labels
    app.kubernetes.io/name: web-app
    app.kubernetes.io/instance: web-app-prod
    app.kubernetes.io/version: "1.2.0"
    app.kubernetes.io/component: frontend
    app.kubernetes.io/part-of: e-commerce
    app.kubernetes.io/managed-by: helm
    # ✅ Custom labels
    environment: production
    team: platform
    cost-center: engineering
```

### 1.3 Estrategias de Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  # ✅ Rolling update strategy
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  
  # ✅ Revision history
  revisionHistoryLimit: 10
  
  template:
    spec:
      # ✅ Pod disruption budget
      terminationGracePeriodSeconds: 30
      
      # ✅ Anti-affinity para alta disponibilidad
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web-app
              topologyKey: kubernetes.io/hostname
```

## 2. **Gestión de Configuración y Secretos**

### 2.1 ConfigMaps
```yaml
# ✅ ConfigMap para configuración no sensible
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  database.properties: |
    database.host=db.production.svc.cluster.local
    database.port=5432
    database.name=myapp
  log-level: "INFO"
  feature-flags.yaml: |
    features:
      new-ui: true
      beta-api: false

---
# Uso en Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: myorg/web-app:latest
        env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: log-level
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
        - name: features-volume
          mountPath: /etc/features
      volumes:
      - name: config-volume
        configMap:
          name: app-config
          items:
          - key: database.properties
            path: database.properties
      - name: features-volume
        configMap:
          name: app-config
          items:
          - key: feature-flags.yaml
            path: features.yaml
```

### 2.2 Secrets Management
```yaml
# ✅ Secret para datos sensibles
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
data:
  # ✅ Valores base64 encoded
  database-password: cGFzc3dvcmQxMjM=
  api-key: YWJjZGVmZ2hpams=

---
# ✅ Uso seguro de secrets
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: myorg/web-app:latest
        env:
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-password
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: api-key
        # ✅ Montar secrets como archivos
        volumeMounts:
        - name: secret-volume
          mountPath: /etc/secrets
          readOnly: true
      volumes:
      - name: secret-volume
        secret:
          secretName: app-secrets
          defaultMode: 0400  # ✅ Permisos restrictivos
```

### 2.3 External Secrets (Recomendado)
```yaml
# ✅ Usar External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.company.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "myapp-role"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 15s
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-password
    remoteRef:
      key: myapp/database
      property: password
  - secretKey: api-key
    remoteRef:
      key: myapp/external-api
      property: key
```

## 3. **Networking y Services**

### 3.1 Services
```yaml
# ✅ Service configuration
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
  namespace: production
  labels:
    app: web-app
  annotations:
    # ✅ Anotaciones para load balancer
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
spec:
  type: LoadBalancer
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  - name: https
    port: 443
    targetPort: 8080
    protocol: TCP
  selector:
    app: web-app
  # ✅ Session affinity si es necesario
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600

---
# ✅ Service interno para comunicación entre servicios
apiVersion: v1
kind: Service
metadata:
  name: web-app-internal
  namespace: production
spec:
  type: ClusterIP
  ports:
  - name: http
    port: 8080
    targetPort: 8080
  selector:
    app: web-app
```

### 3.2 Ingress
```yaml
# ✅ Ingress configuration
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  namespace: production
  annotations:
    # ✅ Ingress controller específico
    kubernetes.io/ingress.class: "nginx"
    # ✅ SSL redirect
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    # ✅ Rate limiting
    nginx.ingress.kubernetes.io/rate-limit: "100"
    # ✅ CORS configuration
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://myapp.com"
    # ✅ Certificate manager
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - myapp.com
    - api.myapp.com
    secretName: myapp-tls
  rules:
  - host: myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app-service
            port:
              number: 80
  - host: api.myapp.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

### 3.3 Network Policies
```yaml
# ✅ Network Policy para seguridad
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-app-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web-app
  policyTypes:
  - Ingress
  - Egress
  
  # ✅ Reglas de ingreso
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8080
  
  # ✅ Reglas de egreso
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to: []  # DNS resolution
    ports:
    - protocol: UDP
      port: 53
  - to:
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
```

## 4. **Persistent Volumes y Storage**

### 4.1 PersistentVolumeClaim
```yaml
# ✅ PVC configuration
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-pvc
  namespace: production
  labels:
    app: database
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd  # ✅ Storage class específico
  resources:
    requests:
      storage: 100Gi
  # ✅ Volume expansion habilitado
  volumeMode: Filesystem

---
# ✅ StatefulSet con PVC
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
  namespace: production
spec:
  serviceName: database-headless
  replicas: 3
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: password
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
  # ✅ Volume claim template
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 50Gi
```

### 4.2 Storage Classes
```yaml
# ✅ Custom Storage Class
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
```

## 5. **Seguridad**

### 5.1 RBAC (Role-Based Access Control)
```yaml
# ✅ ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: web-app-sa
  namespace: production

---
# ✅ Role específico para la aplicación
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: web-app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]

---
# ✅ RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: web-app-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: web-app-sa
  namespace: production
roleRef:
  kind: Role
  name: web-app-role
  apiGroup: rbac.authorization.k8s.io

---
# ✅ Uso en Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      serviceAccountName: web-app-sa
      # ✅ Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 2000
      containers:
      - name: web-app
        image: myorg/web-app:latest
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
```

### 5.2 Pod Security Standards
```yaml
# ✅ Pod Security Policy (deprecated) -> Pod Security Standards
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    # ✅ Pod Security Standards
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
# ✅ Deployment conforme a restricted policy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: production
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: app
        image: myorg/app:latest
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: var-run
          mountPath: /var/run
      volumes:
      - name: tmp
        emptyDir: {}
      - name: var-run
        emptyDir: {}
```

### 5.3 Image Security
```yaml
# ✅ Deployment con image security
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        # ✅ Usar digest específico para inmutabilidad
        image: myorg/web-app@sha256:abc123def456...
        # ✅ Image pull policy
        imagePullPolicy: Always
        
        # ✅ Resource constraints
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      
      # ✅ Image pull secrets
      imagePullSecrets:
      - name: registry-secret
```

## 6. **Monitoring y Observabilidad**

### 6.1 Health Checks
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: myorg/web-app:latest
        ports:
        - containerPort: 8080
        
        # ✅ Liveness probe - reinicia el pod si falla
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
          successThreshold: 1
        
        # ✅ Readiness probe - quita del service si falla
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
          successThreshold: 1
        
        # ✅ Startup probe - para aplicaciones que tardan en iniciar
        startupProbe:
          httpGet:
            path: /actuator/health/startup
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 30
          successThreshold: 1
```

### 6.2 Prometheus Monitoring
```yaml
# ✅ ServiceMonitor para Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: web-app-metrics
  namespace: production
  labels:
    app: web-app
spec:
  selector:
    matchLabels:
      app: web-app
  endpoints:
  - port: metrics
    path: /actuator/prometheus
    interval: 30s
    scrapeTimeout: 10s

---
# ✅ Service con puerto de métricas
apiVersion: v1
kind: Service
metadata:
  name: web-app-metrics
  namespace: production
  labels:
    app: web-app
spec:
  ports:
  - name: metrics
    port: 8080
    targetPort: 8080
  selector:
    app: web-app

---
# ✅ PrometheusRule para alertas
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: web-app-alerts
  namespace: production
spec:
  groups:
  - name: web-app.rules
    rules:
    - alert: WebAppHighErrorRate
      expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High error rate detected"
        description: "Error rate is {{ $value }} for {{ $labels.instance }}"
    
    - alert: WebAppHighLatency
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "High latency detected"
        description: "95th percentile latency is {{ $value }}s"
```

### 6.3 Logging
```yaml
# ✅ Deployment con logging configurado
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: myorg/web-app:latest
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: LOG_FORMAT
          value: "json"
        
        # ✅ Sidecar para logs
      - name: fluentd-sidecar
        image: fluentd:v1.14-debian
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: fluentd-config
          mountPath: /fluentd/etc
        env:
        - name: FLUENTD_CONF
          value: "fluent.conf"
      
      volumes:
      - name: varlog
        emptyDir: {}
      - name: fluentd-config
        configMap:
          name: fluentd-config
```

## 7. **Scaling y Performance**

### 7.1 Horizontal Pod Autoscaler (HPA)
```yaml
# ✅ HPA configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 100
  metrics:
  # ✅ CPU utilization
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # ✅ Memory utilization
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  # ✅ Custom metrics
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  
  # ✅ Scaling behavior
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 4
        periodSeconds: 60
      selectPolicy: Max
```

### 7.2 Vertical Pod Autoscaler (VPA)
```yaml
# ✅ VPA configuration
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-app-vpa
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  updatePolicy:
    updateMode: "Auto"  # Off, Initial, Recreation, Auto
  resourcePolicy:
    containerPolicies:
    - containerName: web-app
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2000m
        memory: 2Gi
      controlledResources: ["cpu", "memory"]
```

### 7.3 Pod Disruption Budget
```yaml
# ✅ PDB para alta disponibilidad
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-app-pdb
  namespace: production
spec:
  minAvailable: 2  # o usar maxUnavailable: 1
  selector:
    matchLabels:
      app: web-app
```

## 8. **Jobs y CronJobs**

### 8.1 Job Configuration
```yaml
# ✅ Job para tareas one-time
apiVersion: batch/v1
kind: Job
metadata:
  name: database-migration-v1-2-0
  namespace: production
  labels:
    app: database-migration
    version: v1.2.0
spec:
  # ✅ TTL para limpieza automática
  ttlSecondsAfterFinished: 86400  # 24 horas
  
  # ✅ Configuración de reintentos
  backoffLimit: 3
  activeDeadlineSeconds: 1800  # 30 minutos
  
  template:
    metadata:
      labels:
        app: database-migration
    spec:
      restartPolicy: Never
      
      # ✅ Init containers para dependencias
      initContainers:
      - name: wait-for-db
        image: busybox:1.35
        command: ['sh', '-c', 'until nc -z database 5432; do sleep 5; done']
      
      containers:
      - name: migrate
        image: myorg/db-migrator:v1.2.0
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        
        # ✅ Security context
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
```

### 8.2 CronJob Configuration
```yaml
# ✅ CronJob para tareas programadas
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
  namespace: production
spec:
  schedule: "0 2 * * *"  # Diario a las 2 AM
  timezone: "America/New_York"
  
  # ✅ Configuración de concurrencia
  concurrencyPolicy: Forbid  # Allow, Forbid, Replace
  
  # ✅ Límites de historial
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  
  # ✅ Deadline para ejecución
  startingDeadlineSeconds: 300
  
  jobTemplate:
    spec:
      ttlSecondsAfterFinished: 86400
      template:
        metadata:
          labels:
            app: database-backup
        spec:
          restartPolicy: OnFailure
          containers:
          - name: backup
            image: postgres:15-alpine
            command:
            - /bin/bash
            - -c
            - |
              pg_dump $DATABASE_URL | gzip > /backup/db-$(date +%Y%m%d-%H%M%S).sql.gz
              # Cleanup old backups (keep last 7 days)
              find /backup -name "db-*.sql.gz" -mtime +7 -delete
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secrets
                  key: url
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
```

## 9. **Namespaces y Multi-tenancy**

### 9.1 Namespace Organization
```yaml
# ✅ Namespace con labels y resource quotas
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    team: platform
    cost-center: engineering
    # ✅ Pod security standards
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
# ✅ Resource Quota por namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    # ✅ Límites de recursos
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    
    # ✅ Límites de objetos
    pods: "50"
    services: "10"
    secrets: "20"
    configmaps: "20"
    persistentvolumeclaims: "10"
    
    # ✅ Límites de storage
    requests.storage: 100Gi

---
# ✅ Limit Range para defaults
apiVersion: v1
kind: LimitRange
metadata:
  name: production-limits
  namespace: production
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "250m"
      memory: "256Mi"
    type: Container
  - max:
      cpu: "2000m"
      memory: "2Gi"
    min:
      cpu: "100m"
      memory: "128Mi"
    type: Container
```

## 10. **GitOps y CI/CD**

### 10.1 Kustomization
```yaml
# ✅ kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

metadata:
  name: web-app-production

# ✅ Common labels
commonLabels:
  app: web-app
  environment: production

# ✅ Common annotations
commonAnnotations:
  managed-by: kustomize
  version: v1.2.0

# ✅ Resources
resources:
- deployment.yaml
- service.yaml
- ingress.yaml
- configmap.yaml
- secret.yaml
- hpa.yaml
- pdb.yaml

# ✅ Patches
patchesStrategicMerge:
- production-patches.yaml

# ✅ Images
images:
- name: myorg/web-app
  newTag: v1.2.0

# ✅ Config generator
configMapGenerator:
- name: app-config
  files:
  - config/application.properties
  - config/logback.xml

# ✅ Secret generator
secretGenerator:
- name: app-secrets
  envs:
  - secrets/.env
```

### 10.2 ArgoCD Application
```yaml
# ✅ ArgoCD Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web-app-production
  namespace: argocd
  finalizers:
  - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  
  # ✅ Source configuration
  source:
    repoURL: https://github.com/myorg/k8s-manifests
    targetRevision: main
    path: apps/web-app/overlays/production
  
  # ✅ Destination
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  
  # ✅ Sync policy
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  
  # ✅ Health checks
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas  # Ignore HPA changes
```

### 10.3 GitHub Actions CI/CD
```yaml
# ✅ .github/workflows/deploy.yml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      
    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=sha,prefix={{branch}}-

    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Update Kubernetes manifests
      run: |
        # Update image tag in kustomization
        cd k8s/overlays/production
        kustomize edit set image ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.meta.outputs.tags }}
        
        # Commit changes
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git commit -m "Update image to ${{ steps.meta.outputs.tags }}"
        git push
```

## 11. **Troubleshooting y Debugging**

### 11.1 Comandos Útiles
```bash
# ✅ Información de pods
kubectl get pods -o wide --show-labels
kubectl describe pod <pod-name>
kubectl logs <pod-name> -f --previous

# ✅ Debugging de recursos
kubectl explain deployment.spec.template.spec.containers
kubectl get events --sort-by=.metadata.creationTimestamp

# ✅ Debug de networking
kubectl exec -it <pod-name> -- nslookup <service-name>
kubectl exec -it <pod-name> -- wget -qO- <service-name>:8080/health

# ✅ Resource usage
kubectl top pods --all-namespaces
kubectl top nodes

# ✅ Dry run para validar
kubectl apply --dry-run=client -f deployment.yaml
kubectl apply --dry-run=server -f deployment.yaml

# ✅ Port forwarding para debugging
kubectl port-forward pod/<pod-name> 8080:8080
kubectl port-forward service/<service-name> 8080:80

# ✅ Troubleshooting de recursos
kubectl get pods --field-selector=status.phase=Pending
kubectl get pods --field-selector=status.phase=Failed
```

### 11.2 Debug Pod
```yaml
# ✅ Debug pod para troubleshooting
apiVersion: v1
kind: Pod
metadata:
  name: debug-pod
  namespace: production
spec:
  containers:
  - name: debug
    image: nicolaka/netshoot
    command: ["/bin/bash"]
    args: ["-c", "sleep 3600"]
    securityContext:
      capabilities:
        add: ["NET_ADMIN"]
  restartPolicy: Never

# Usar con:
# kubectl exec -it debug-pod -- bash
```

## 12. **Herramientas y Utilidades**

### 12.1 Herramientas de CLI
```bash
# ✅ Herramientas esenciales
# kubectl - CLI principal de Kubernetes
# helm - Package manager
# kustomize - Configuration management
# kubectx/kubens - Context y namespace switching
# k9s - Terminal UI para Kubernetes
# stern - Multi-pod log tailing
# kubeval - Validation tool
# kube-score - Best practices analyzer

# Instalación con package managers
brew install kubectl helm kustomize kubectx k9s stern
```

### 12.2 Configuración de kubectl
```bash
# ✅ ~/.kube/config organization
kubectl config set-context prod --namespace=production --cluster=prod-cluster --user=prod-user
kubectl config use-context prod

# ✅ Aliases útiles
alias k=kubectl
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kdp='kubectl describe pod'
alias kl='kubectl logs -f'

# ✅ Autocompletion
source <(kubectl completion bash)
# o para zsh
source <(kubectl completion zsh)
```

---

## Checklist de Mejores Prácticas

### ✅ Configuración de Recursos
- [ ] Especificar requests y limits para CPU y memoria
- [ ] Configurar health checks (liveness, readiness, startup)
- [ ] Usar labels y annotations consistentes
- [ ] Implementar security contexts apropiados

### ✅ Seguridad
- [ ] Usar ServiceAccounts específicos con RBAC
- [ ] Implementar Network Policies
- [ ] Usar Secrets para datos sensibles
- [ ] Aplicar Pod Security Standards
- [ ] No ejecutar como root

### ✅ Alta Disponibilidad
- [ ] Configurar anti-affinity rules
- [ ] Implementar Pod Disruption Budgets
- [ ] Usar múltiples replicas
- [ ] Configurar HPA cuando sea apropiado

### ✅ Monitoreo
- [ ] Configurar ServiceMonitor para Prometheus
- [ ] Implementar alertas críticas
- [ ] Configurar logging estructurado
- [ ] Exponer métricas de aplicación

### ✅ Storage
- [ ] Usar StorageClasses apropiados
- [ ] Configurar backup strategies
- [ ] Implementar Volume expansion si es necesario

### ✅ Networking
- [ ] Usar Services apropiados (ClusterIP, LoadBalancer, etc.)
- [ ] Configurar Ingress con TLS
- [ ] Implementar Network Policies
- [ ] Considerar service mesh para arquitecturas complejas

## Recursos Adicionales

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Best Practices by Google](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [CNCF Landscape](https://landscape.cncf.io/)
- [Helm Charts Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Kustomize Documentation](https://kustomize.io/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)

---

*Última actualización: Junio 2025*

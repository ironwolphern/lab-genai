---
applyTo: "**/*.yaml,**/*.yml,**/*.json"
---
# Buenas Prácticas de OpenShift

## 1. **Fundamentos de OpenShift vs Kubernetes**

### 1.1 Diferencias Clave
- OpenShift añade capas de seguridad, automatización y herramientas de desarrollo sobre Kubernetes
- Incluye registro de imágenes integrado, pipelines CI/CD, y herramientas de monitoreo
- Enforza Security Context Constraints (SCCs) más estrictos que Kubernetes vanilla
- Proporciona Routes como abstracción sobre Ingress

### 1.2 Arquitectura de OpenShift
```yaml
# ✅ Jerarquía de OpenShift
Cluster
├── Projects (Namespaces con funcionalidades adicionales)
│   ├── Applications
│   │   ├── DeploymentConfigs / Deployments
│   │   ├── Services
│   │   ├── Routes
│   │   └── BuildConfigs
│   ├── Image Streams
│   └── Templates
```

## 2. **Projects y Namespaces**

### 2.1 Gestión de Projects
```yaml
# ✅ Project con configuración completa
apiVersion: project.openshift.io/v1
kind: Project
metadata:
  name: myapp-production
  annotations:
    # ✅ Descripción del proyecto
    openshift.io/description: "Production environment for MyApp"
    openshift.io/display-name: "MyApp Production"
    openshift.io/requester: "platform-team"
  labels:
    # ✅ Labels para organización
    environment: production
    team: platform
    cost-center: engineering
    project-type: application

---
# ✅ Project Request Template personalizado
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: project-request
  namespace: openshift-config
objects:
- apiVersion: project.openshift.io/v1
  kind: Project
  metadata:
    name: ${PROJECT_NAME}
    annotations:
      openshift.io/description: ${PROJECT_DESCRIPTION}
      openshift.io/display-name: ${PROJECT_DISPLAYNAME}
    labels:
      environment: ${ENVIRONMENT}
      team: ${TEAM}
- apiVersion: rbac.authorization.k8s.io/v1
  kind: RoleBinding
  metadata:
    name: admin
    namespace: ${PROJECT_NAME}
  roleRef:
    apiGroup: rbac.authorization.k8s.io
    kind: ClusterRole
    name: admin
  subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: User
    name: ${PROJECT_ADMIN_USER}
parameters:
- name: PROJECT_NAME
  displayName: Project Name
  description: The name of the project
  required: true
- name: PROJECT_DESCRIPTION
  displayName: Project Description  
  description: A description for the project
- name: PROJECT_DISPLAYNAME
  displayName: Project Display Name
  description: The display name of the project
- name: ENVIRONMENT
  displayName: Environment
  description: Environment type (dev, test, prod)
  required: true
- name: TEAM
  displayName: Team
  description: Team responsible for the project
  required: true
- name: PROJECT_ADMIN_USER
  displayName: Project Admin User
  description: User to be granted admin access
  required: true
```

### 2.2 Resource Quotas y Limits
```yaml
# ✅ ResourceQuota para Projects
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: myapp-production
spec:
  hard:
    # ✅ Límites de compute
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    
    # ✅ Límites de objetos OpenShift
    pods: "50"
    services: "20"
    routes.route.openshift.io: "10"
    imagestreams.image.openshift.io: "20"
    buildconfigs.build.openshift.io: "10"
    
    # ✅ Límites de storage
    requests.storage: 500Gi
    persistentvolumeclaims: "20"

---
# ✅ LimitRange con valores por defecto
apiVersion: v1
kind: LimitRange
metadata:
  name: production-limits
  namespace: myapp-production
spec:
  limits:
  - default:
      cpu: "1000m"
      memory: "1Gi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "4000m"
      memory: "8Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
    type: Container
  - max:
      cpu: "8000m"
      memory: "16Gi"
    min:
      cpu: "100m"
      memory: "128Mi"
    type: Pod
```

## 3. **Security Context Constraints (SCCs)**

### 3.1 SCC Custom
```yaml
# ✅ Custom SCC para aplicaciones específicas
apiVersion: security.openshift.io/v1
kind: SecurityContextConstraints
metadata:
  name: myapp-scc
  annotations:
    kubernetes.io/description: "SCC for MyApp with specific security requirements"
allowHostDirVolumePlugin: false
allowHostIPC: false
allowHostNetwork: false
allowHostPID: false
allowHostPorts: false
allowPrivilegeEscalation: false
allowPrivilegedContainer: false
allowedCapabilities: []
defaultAddCapabilities: []
fsGroup:
  type: MustRunAs
  ranges:
  - min: 1000
    max: 65535
readOnlyRootFilesystem: false
requiredDropCapabilities:
- ALL
runAsUser:
  type: MustRunAsRange
  uidRangeMin: 1000
  uidRangeMax: 65535
seLinuxContext:
  type: MustRunAs
supplementalGroups:
  type: MustRunAs
  ranges:
  - min: 1000
    max: 65535
volumes:
- configMap
- emptyDir
- persistentVolumeClaim
- projected
- secret
priority: 10

---
# ✅ ServiceAccount con SCC específico
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: myapp-production

---
# ✅ ClusterRoleBinding para SCC
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: myapp-scc-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:openshift:scc:myapp-scc
subjects:
- kind: ServiceAccount
  name: myapp-sa
  namespace: myapp-production
```

### 3.2 Deployment con SCC
```yaml
# ✅ Deployment usando SCC personalizado
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: myapp-production
  labels:
    app: myapp
    version: v1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.0.0
    spec:
      serviceAccountName: myapp-sa
      
      # ✅ Security context compatible con OpenShift SCCs
      securityContext:
        runAsNonRoot: true
        # No especificar runAsUser - OpenShift lo asignará automáticamente
        fsGroup: 1000
      
      containers:
      - name: myapp
        image: image-registry.openshift-image-registry.svc:5000/myapp-production/myapp:v1.0.0
        ports:
        - containerPort: 8080
          protocol: TCP
        
        # ✅ Security context del container
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true
        
        # ✅ Resources siempre especificados
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        
        # ✅ Health checks
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        
        # ✅ Variables de entorno
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: PORT
          value: "8080"
        
        # ✅ Volúmenes para filesystem read-only
        volumeMounts:
        - name: tmp-volume
          mountPath: /tmp
        - name: cache-volume
          mountPath: /app/cache
      
      volumes:
      - name: tmp-volume
        emptyDir: {}
      - name: cache-volume
        emptyDir: {}
```

## 4. **Image Streams y Build Configs**

### 4.1 ImageStream Configuration
```yaml
# ✅ ImageStream para aplicación
apiVersion: image.openshift.io/v1
kind: ImageStream
metadata:
  name: myapp
  namespace: myapp-production
  labels:
    app: myapp
spec:
  lookupPolicy:
    local: true  # ✅ Permite lookup local de imágenes
  tags:
  - name: latest
    from:
      kind: DockerImage
      name: registry.redhat.io/ubi8/nodejs-16:latest
    importPolicy:
      scheduled: true  # ✅ Import automático de updates
      insecure: false
    referencePolicy:
      type: Source

---
# ✅ ImageStream para imagen base
apiVersion: image.openshift.io/v1
kind: ImageStream
metadata:
  name: nodejs-16-ubi8
  namespace: myapp-production
spec:
  tags:
  - name: latest
    from:
      kind: DockerImage
      name: registry.redhat.io/ubi8/nodejs-16:latest
    importPolicy:
      scheduled: true
      importMode: Legacy
    referencePolicy:
      type: Source
```

### 4.2 BuildConfig S2I (Source-to-Image)
```yaml
# ✅ BuildConfig con Source-to-Image
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: myapp
  namespace: myapp-production
  labels:
    app: myapp
spec:
  # ✅ Triggers automáticos
  triggers:
  - type: ConfigChange
  - type: ImageChange
    imageChange:
      from:
        kind: ImageStreamTag
        name: nodejs-16-ubi8:latest
  - type: GitHub
    github:
      secret: github-webhook-secret
  
  # ✅ Configuración de Source
  source:
    type: Git
    git:
      uri: https://github.com/myorg/myapp.git
      ref: main
    contextDir: /
    secrets:
    - secret:
        name: git-credentials
      destinationDir: /tmp
  
  # ✅ Estrategia S2I
  strategy:
    type: Source
    sourceStrategy:
      from:
        kind: ImageStreamTag
        name: nodejs-16-ubi8:latest
      env:
      - name: NPM_MIRROR
        value: https://registry.npmjs.org
      - name: NODE_ENV
        value: production
      # ✅ Scripts personalizados
      scripts: https://github.com/myorg/s2i-scripts.git
      incremental: true  # ✅ Builds incrementales
  
  # ✅ Output a ImageStream
  output:
    to:
      kind: ImageStreamTag
      name: myapp:latest
    pushSecret:
      name: registry-credentials
  
  # ✅ Resource limits para builds
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 1000m
      memory: 1Gi
  
  # ✅ Configuración de completado
  completionDeadlineSeconds: 1800  # 30 minutos
  successfulBuildsHistoryLimit: 5
  failedBuildsHistoryLimit: 3
```

### 4.3 BuildConfig Docker Strategy
```yaml
# ✅ BuildConfig con Docker strategy
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: myapp-docker
  namespace: myapp-production
spec:
  triggers:
  - type: ConfigChange
  - type: ImageChange
  
  source:
    type: Git
    git:
      uri: https://github.com/myorg/myapp.git
      ref: main
    dockerfile: |
      FROM registry.redhat.io/ubi8/nodejs-16:latest
      
      USER 0
      
      # Install dependencies
      COPY package*.json ./
      RUN npm ci --only=production && npm cache clean --force
      
      # Copy application code
      COPY . .
      
      # Create non-root user compatible with OpenShift
      RUN chgrp -R 0 /opt/app-root && \
          chmod -R g=u /opt/app-root
      
      USER 1001
      
      EXPOSE 8080
      
      CMD ["npm", "start"]
  
  strategy:
    type: Docker
    dockerStrategy:
      dockerfilePath: Dockerfile
      env:
      - name: HTTP_PROXY
        value: "${HTTP_PROXY}"
      - name: HTTPS_PROXY
        value: "${HTTPS_PROXY}"
  
  output:
    to:
      kind: ImageStreamTag
      name: myapp:latest
```

## 5. **DeploymentConfigs vs Deployments**

### 5.1 DeploymentConfig (OpenShift específico)
```yaml
# ✅ DeploymentConfig con triggers automáticos
apiVersion: apps.openshift.io/v1
kind: DeploymentConfig
metadata:
  name: myapp-dc
  namespace: myapp-production
  labels:
    app: myapp
spec:
  replicas: 3
  
  # ✅ Triggers específicos de OpenShift
  triggers:
  - type: ConfigChange
  - type: ImageChange
    imageChangeParams:
      automatic: true
      containerNames:
      - myapp
      from:
        kind: ImageStreamTag
        name: myapp:latest
        namespace: myapp-production
  
  # ✅ Estrategia de deployment
  strategy:
    type: Rolling
    rollingParams:
      maxUnavailable: 1
      maxSurge: 1
      timeoutSeconds: 600
      updatePeriodSeconds: 1
      intervalSeconds: 1
      pre:
        failurePolicy: Abort
        execNewPod:
          command:
          - /bin/sh
          - -c
          - echo "Pre-deployment hook"
          containerName: myapp
      post:
        failurePolicy: Ignore
        execNewPod:
          command:
          - /bin/sh
          - -c
          - echo "Post-deployment hook"
          containerName: myapp
  
  selector:
    app: myapp
    deploymentconfig: myapp-dc
  
  template:
    metadata:
      labels:
        app: myapp
        deploymentconfig: myapp-dc
    spec:
      containers:
      - name: myapp
        image: myapp:latest  # ✅ Será reemplazado por trigger
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
```

### 5.2 Cuándo usar DeploymentConfig vs Deployment
```yaml
# ✅ Usar DeploymentConfig cuando:
# - Necesites triggers automáticos de ImageStream
# - Requieras hooks de pre/post deployment
# - Uses S2I builds integrados
# - Necesites rolling back automático

# ✅ Usar Deployment cuando:
# - Quieras compatibilidad total con Kubernetes
# - Uses herramientas de GitOps (ArgoCD, Flux)
# - Prefieras control manual de deployments
# - Trabajes con ecosistema Kubernetes estándar

apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  namespace: myapp-production
  annotations:
    # ✅ Trigger manual con image updater
    image.openshift.io/triggers: |
      [
        {
          "from": {
            "kind": "ImageStreamTag",
            "name": "myapp:latest"
          },
          "fieldPath": "spec.template.spec.containers[?(@.name==\"myapp\")].image"
        }
      ]
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: image-registry.openshift-image-registry.svc:5000/myapp-production/myapp:latest
        # ... resto de la configuración
```

## 6. **Routes y Networking**

### 6.1 Route Configuration
```yaml
# ✅ Route básico con TLS
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: myapp-route
  namespace: myapp-production
  labels:
    app: myapp
  annotations:
    # ✅ HAProxy annotations
    haproxy.router.openshift.io/timeout: 30s
    haproxy.router.openshift.io/rate-limit-connections: "true"
    haproxy.router.openshift.io/rate-limit-connections.concurrent-tcp: "100"
    haproxy.router.openshift.io/rate-limit-connections.rate-http: "100"
spec:
  host: myapp.apps.cluster.example.com
  to:
    kind: Service
    name: myapp-service
    weight: 100
  port:
    targetPort: 8080-tcp
  
  # ✅ TLS Configuration
  tls:
    termination: edge
    certificate: |
      -----BEGIN CERTIFICATE-----
      ...
      -----END CERTIFICATE-----
    key: |
      -----BEGIN PRIVATE KEY-----
      ...
      -----END PRIVATE KEY-----
    caCertificate: |
      -----BEGIN CERTIFICATE-----
      ...
      -----END CERTIFICATE-----
    insecureEdgeTerminationPolicy: Redirect

---
# ✅ Route con múltiples servicios (Blue-Green)
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: myapp-bluegreen
  namespace: myapp-production
spec:
  host: myapp.apps.cluster.example.com
  to:
    kind: Service
    name: myapp-blue
    weight: 90
  alternateBackends:
  - kind: Service
    name: myapp-green
    weight: 10
  port:
    targetPort: 8080-tcp
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
```

### 6.2 Service Configuration
```yaml
# ✅ Service para aplicación
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: myapp-production
  labels:
    app: myapp
  annotations:
    # ✅ Service annotations para OpenShift
    service.alpha.openshift.io/serving-cert-secret-name: myapp-tls
    service.beta.openshift.io/serving-cert-signed-by: openshift-service-ca@1234567890
spec:
  type: ClusterIP
  ports:
  - name: 8080-tcp
    port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    app: myapp
    deploymentconfig: myapp-dc
  sessionAffinity: None

---
# ✅ Service para métricas
apiVersion: v1
kind: Service
metadata:
  name: myapp-metrics
  namespace: myapp-production
  labels:
    app: myapp
spec:
  type: ClusterIP
  ports:
  - name: metrics
    port: 9090
    protocol: TCP
    targetPort: 9090
  selector:
    app: myapp
```

## 7. **Templates y Helm Charts**

### 7.1 OpenShift Template
```yaml
# ✅ Template completo para aplicación
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: myapp-template
  namespace: myapp-production
  annotations:
    description: "Template for deploying MyApp"
    tags: "nodejs,javascript,web"
    iconClass: "icon-nodejs"
    openshift.io/display-name: "MyApp"
    openshift.io/documentation-url: "https://docs.myapp.com"
    openshift.io/support-url: "https://support.myapp.com"
objects:

# ✅ ImageStream
- apiVersion: image.openshift.io/v1
  kind: ImageStream
  metadata:
    name: ${APPLICATION_NAME}
    namespace: ${NAMESPACE}
    labels:
      app: ${APPLICATION_NAME}

# ✅ BuildConfig
- apiVersion: build.openshift.io/v1
  kind: BuildConfig
  metadata:
    name: ${APPLICATION_NAME}
    namespace: ${NAMESPACE}
    labels:
      app: ${APPLICATION_NAME}
  spec:
    triggers:
    - type: ConfigChange
    - type: ImageChange
    source:
      type: Git
      git:
        uri: ${SOURCE_REPOSITORY_URL}
        ref: ${SOURCE_REPOSITORY_REF}
    strategy:
      type: Source
      sourceStrategy:
        from:
          kind: ImageStreamTag
          name: nodejs-16-ubi8:latest
          namespace: openshift
        env:
        - name: NODE_ENV
          value: ${NODE_ENV}
    output:
      to:
        kind: ImageStreamTag
        name: ${APPLICATION_NAME}:latest

# ✅ DeploymentConfig
- apiVersion: apps.openshift.io/v1
  kind: DeploymentConfig
  metadata:
    name: ${APPLICATION_NAME}
    namespace: ${NAMESPACE}
    labels:
      app: ${APPLICATION_NAME}
  spec:
    replicas: ${{REPLICA_COUNT}}
    triggers:
    - type: ConfigChange
    - type: ImageChange
      imageChangeParams:
        automatic: true
        containerNames:
        - ${APPLICATION_NAME}
        from:
          kind: ImageStreamTag
          name: ${APPLICATION_NAME}:latest
    selector:
      app: ${APPLICATION_NAME}
      deploymentconfig: ${APPLICATION_NAME}
    template:
      metadata:
        labels:
          app: ${APPLICATION_NAME}
          deploymentconfig: ${APPLICATION_NAME}
      spec:
        containers:
        - name: ${APPLICATION_NAME}
          image: ${APPLICATION_NAME}:latest
          ports:
          - containerPort: ${{APPLICATION_PORT}}
            protocol: TCP
          resources:
            requests:
              cpu: ${CPU_REQUEST}
              memory: ${MEMORY_REQUEST}
            limits:
              cpu: ${CPU_LIMIT}
              memory: ${MEMORY_LIMIT}
          env:
          - name: NODE_ENV
            value: ${NODE_ENV}
          - name: PORT
            value: ${APPLICATION_PORT}
          livenessProbe:
            httpGet:
              path: /health
              port: ${{APPLICATION_PORT}}
            initialDelaySeconds: 30
          readinessProbe:
            httpGet:
              path: /ready
              port: ${{APPLICATION_PORT}}
            initialDelaySeconds: 5

# ✅ Service
- apiVersion: v1
  kind: Service
  metadata:
    name: ${APPLICATION_NAME}
    namespace: ${NAMESPACE}
    labels:
      app: ${APPLICATION_NAME}
  spec:
    ports:
    - name: ${APPLICATION_PORT}-tcp
      port: ${{APPLICATION_PORT}}
      protocol: TCP
      targetPort: ${{APPLICATION_PORT}}
    selector:
      app: ${APPLICATION_NAME}
      deploymentconfig: ${APPLICATION_NAME}

# ✅ Route
- apiVersion: route.openshift.io/v1
  kind: Route
  metadata:
    name: ${APPLICATION_NAME}
    namespace: ${NAMESPACE}
    labels:
      app: ${APPLICATION_NAME}
  spec:
    host: ${APPLICATION_DOMAIN}
    to:
      kind: Service
      name: ${APPLICATION_NAME}
    port:
      targetPort: ${APPLICATION_PORT}-tcp
    tls:
      termination: edge
      insecureEdgeTerminationPolicy: Redirect

# ✅ Parameters
parameters:
- name: APPLICATION_NAME
  displayName: Application Name
  description: The name assigned to all application components
  value: myapp
  required: true

- name: NAMESPACE
  displayName: Namespace
  description: The OpenShift Namespace where the application resides
  required: true

- name: SOURCE_REPOSITORY_URL
  displayName: Git Repository URL
  description: The URL of the repository with your application source code
  required: true

- name: SOURCE_REPOSITORY_REF
  displayName: Git Reference
  description: Set this to a branch name, tag or other ref of your repository
  value: main

- name: APPLICATION_DOMAIN
  displayName: Application Hostname
  description: The exposed hostname that will route to the service

- name: APPLICATION_PORT
  displayName: Application Port
  description: Port that application is listening on for traffic
  value: "8080"
  required: true

- name: REPLICA_COUNT
  displayName: Replica Count
  description: Number of replicas to run
  value: "3"
  required: true

- name: CPU_REQUEST
  displayName: CPU Request
  description: The requested CPU for each replica
  value: 100m

- name: CPU_LIMIT
  displayName: CPU Limit
  description: The maximum CPU for each replica
  value: 500m

- name: MEMORY_REQUEST
  displayName: Memory Request
  description: The requested memory for each replica
  value: 256Mi

- name: MEMORY_LIMIT
  displayName: Memory Limit
  description: The maximum memory for each replica
  value: 512Mi

- name: NODE_ENV
  displayName: Node Environment
  description: Environment for Node.js application
  value: production

# ✅ Labels para el template
labels:
  template: myapp-template
  app: myapp
```

### 7.2 Uso de Templates
```bash
# ✅ Procesar template
oc process -f myapp-template.yaml \
  -p APPLICATION_NAME=myapp \
  -p NAMESPACE=myapp-production \
  -p SOURCE_REPOSITORY_URL=https://github.com/myorg/myapp.git \
  -p APPLICATION_DOMAIN=myapp.apps.cluster.example.com \
  | oc apply -f -

# ✅ Crear template en cluster
oc create -f myapp-template.yaml -n openshift

# ✅ Instanciar template desde cluster
oc new-app --template=myapp-template \
  -p APPLICATION_NAME=myapp-prod \
  -p NAMESPACE=myapp-production
```

## 8. **Pipelines CI/CD con Tekton**

### 8.1 Pipeline Configuration
```yaml
# ✅ Tekton Pipeline para OpenShift
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: myapp-pipeline
  namespace: myapp-production
spec:
  description: |
    Pipeline for building and deploying MyApp to OpenShift
  
  params:
  - name: git-url
    type: string
    description: Git repository URL
  - name: git-revision
    type: string
    description: Git revision to build
    default: main
  - name: image-name
    type: string
    description: Output image name
  - name: image-tag
    type: string
    description: Output image tag
    default: latest
  
  workspaces:
  - name: shared-data
    description: Shared workspace for pipeline
  - name: git-credentials
    description: Git credentials
    optional: true
  
  tasks:
  # ✅ Task 1: Git Clone
  - name: fetch-source
    taskRef:
      name: git-clone
      kind: ClusterTask
    workspaces:
    - name: output
      workspace: shared-data
    - name: ssh-directory
      workspace: git-credentials
    params:
    - name: url
      value: $(params.git-url)
    - name: revision
      value: $(params.git-revision)
  
  # ✅ Task 2: Run Tests
  - name: test
    runAfter: ["fetch-source"]
    taskRef:
      name: npm
      kind: ClusterTask
    workspaces:
    - name: source
      workspace: shared-data
    params:
    - name: ARGS
      value: ["test"]
  
  # ✅ Task 3: Security Scan
  - name: security-scan
    runAfter: ["fetch-source"]
    taskRef:
      name: trivy-scanner
      kind: ClusterTask
    workspaces:
    - name: source
      workspace: shared-data
  
  # ✅ Task 4: Build Image with S2I
  - name: build-image
    runAfter: ["test", "security-scan"]
    taskRef:
      name: s2i-nodejs
      kind: ClusterTask
    workspaces:
    - name: source
      workspace: shared-data
    params:
    - name: IMAGE
      value: $(params.image-name):$(params.image-tag)
    - name: BUILDER_IMAGE
      value: registry.redhat.io/ubi8/nodejs-16:latest
  
  # ✅ Task 5: Update Image Tag
  - name: update-deployment
    runAfter: ["build-image"]
    taskRef:
      name: openshift-client
      kind: ClusterTask
    params:
    - name: SCRIPT
      value: |
        oc tag $(params.image-name):$(params.image-tag) $(params.image-name):production
        oc rollout status dc/myapp -w

---
# ✅ PipelineRun
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  generateName: myapp-pipeline-run-
  namespace: myapp-production
spec:
  pipelineRef:
    name: myapp-pipeline
  
  params:
  - name: git-url
    value: https://github.com/myorg/myapp.git
  - name: git-revision
    value: main
  - name: image-name
    value: image-registry.openshift-image-registry.svc:5000/myapp-production/myapp
  - name: image-tag
    value: $(context.pipelineRun.name)
  
  workspaces:
  - name: shared-data
    volumeClaimTemplate:
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 1Gi
  - name: git-credentials
    secret:
      secretName: git-credentials
```

### 8.2 Triggers para Webhooks
```yaml
# ✅ TriggerTemplate
apiVersion: triggers.tekton.dev/v1beta1
kind: TriggerTemplate
metadata:
  name: myapp-trigger-template
  namespace: myapp-production
spec:
  params:
  - name: git-repo-url
    description: The git repository url
  - name: git-revision
    description: The git revision
    default: main
  - name: git-repo-name
    description: The name of the deployment to be created / patched

  resourcetemplates:
  - apiVersion: tekton.dev/v1beta1
    kind: PipelineRun
    metadata:
      generateName: myapp-pipeline-run-
    spec:
      pipelineRef:
        name: myapp-pipeline
      params:
      - name: git-url
        value: $(tt.params.git-repo-url)
      - name: git-revision
        value: $(tt.params.git-revision)
      - name: image-name
        value: image-registry.openshift-image-registry.svc:5000/myapp-production/myapp
      - name: image-tag
        value: $(tt.params.git-revision)
      workspaces:
      - name: shared-data
        volumeClaimTemplate:
          spec:
            accessModes:
            - ReadWriteOnce
            resources:
              requests:
                storage: 1Gi

---
# ✅ TriggerBinding
apiVersion: triggers.tekton.dev/v1beta1
kind: TriggerBinding
metadata:
  name: myapp-trigger-binding
  namespace: myapp-production
spec:
  params:
  - name: git-repo-url
    value: $(body.repository.url)
  - name: git-repo-name
    value: $(body.repository.name)
  - name: git-revision
    value: $(body.head_commit.id)

---
# ✅ EventListener
apiVersion: triggers.tekton.dev/v1beta1
kind: EventListener
metadata:
  name: myapp-event-listener
  namespace: myapp-production
spec:
  serviceAccountName: pipeline
  triggers:
  - name: github-listener
    bindings:
    - ref: myapp-trigger-binding
    template:
      ref: myapp-trigger-template
    interceptors:
    - name: github
      params:
      - name: secretRef
        value:
          secretName: github-webhook-secret
          secretKey: secretToken
      - name: eventTypes
        value: ["push"]
```

## 9. **Monitoring y Logging**

### 9.1 Prometheus ServiceMonitor
```yaml
# ✅ ServiceMonitor para aplicación
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp-metrics
  namespace: myapp-production
  labels:
    app: myapp
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s
    scrapeTimeout: 10s
    scheme: https
    tlsConfig:
      caFile: /etc/prometheus/configmaps/serving-certs-ca-bundle/service-ca.crt
      serverName: myapp-metrics.myapp-production.svc

---
# ✅ PrometheusRule para alertas
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-alerts
  namespace: myapp-production
  labels:
    app: myapp
spec:
  groups:
  - name: myapp.rules
    rules:
    - alert: MyAppHighErrorRate
      expr: |
        rate(http_requests_total{job="myapp-metrics",status=~"5.."}[5m]) > 0.1
      for: 5m
      labels:
        severity: warning
        service: myapp
      annotations:
        summary: "MyApp high error rate"
        description: "Error rate is {{ $value }} for {{ $labels.instance }}"
    
    - alert: MyAppHighLatency
      expr: |
        histogram_quantile(0.95, 
          rate(http_request_duration_seconds_bucket{job="myapp-metrics"}[5m])
        ) > 0.5
      for: 10m
      labels:
        severity: warning
        service: myapp
      annotations:
        summary: "MyApp high latency"
        description: "95th percentile latency is {{ $value }}s"
    
    - alert: MyAppPodCrashLooping
      expr: |
        rate(kube_pod_container_status_restarts_total{
          namespace="myapp-production",
          pod=~"myapp-.*"
        }[5m]) > 0
      for: 5m
      labels:
        severity: critical
        service: myapp
      annotations:
        summary: "MyApp pod crash looping"
        description: "Pod {{ $labels.pod }} is crash looping"
```

### 9.2 Cluster Logging
```yaml
# ✅ ClusterLogForwarder para logs específicos
apiVersion: logging.coreos.com/v1
kind: ClusterLogForwarder
metadata:
  name: myapp-logs
  namespace: openshift-logging
spec:
  outputs:
  - name: myapp-elasticsearch
    type: elasticsearch
    url: https://elasticsearch.example.com:9200
    secret:
      name: elasticsearch-credentials
  
  - name: myapp-splunk
    type: splunk
    url: https://splunk.example.com:8088
    secret:
      name: splunk-credentials
  
  pipelines:
  - name: myapp-application-logs
    inputRefs:
    - application
    filterRefs:
    - myapp-filter
    outputRefs:
    - myapp-elasticsearch
    - myapp-splunk
  
  filters:
  - name: myapp-filter
    type: json
    json:
      javascript: |
        const log = record.log;
        if (log && log.kubernetes && 
            log.kubernetes.namespace_name === "myapp-production") {
          return record;
        }
        return null;
```

## 10. **Storage y Persistent Volumes**

### 10.1 StorageClass para OpenShift
```yaml
# ✅ Custom StorageClass
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd-retain
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
  kmsKeyId: "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Retain  # ✅ Retain para datos críticos
mountOptions:
- debug
```

### 10.2 StatefulSet con PVC
```yaml
# ✅ StatefulSet para base de datos
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql
  namespace: myapp-production
spec:
  serviceName: postgresql-headless
  replicas: 3
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      # ✅ Security context para OpenShift
      securityContext:
        fsGroup: 26
        runAsUser: 26
      
      containers:
      - name: postgresql
        image: registry.redhat.io/rhel8/postgresql-13:latest
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRESQL_DATABASE
          value: myapp
        - name: POSTGRESQL_USER
          valueFrom:
            secretKeyRef:
              name: postgresql-credentials
              key: username
        - name: POSTGRESQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgresql-credentials
              key: password
        - name: PGDATA
          value: /var/lib/pgsql/data/pgdata
        
        # ✅ Resources apropiados para DB
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        
        # ✅ Health checks para DB
        livenessProbe:
          exec:
            command:
            - /usr/libexec/check-container
            - --live
          initialDelaySeconds: 120
          timeoutSeconds: 10
        readinessProbe:
          exec:
            command:
            - /usr/libexec/check-container
          initialDelaySeconds: 5
          timeoutSeconds: 1
        
        volumeMounts:
        - name: postgresql-data
          mountPath: /var/lib/pgsql/data
        - name: postgresql-config
          mountPath: /opt/app-root/src/postgresql-cfg
      
      volumes:
      - name: postgresql-config
        configMap:
          name: postgresql-config
  
  # ✅ Volume claim template
  volumeClaimTemplates:
  - metadata:
      name: postgresql-data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd-retain
      resources:
        requests:
          storage: 100Gi
```

## 11. **Network Policies**

### 11.1 Network Policy para Microsegmentación
```yaml
# ✅ Default deny all
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: myapp-production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
# ✅ Allow ingress desde router
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-openshift-ingress
  namespace: myapp-production
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          network.openshift.io/policy-group: ingress
    ports:
    - protocol: TCP
      port: 8080

---
# ✅ Allow egress to database
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp-to-database
  namespace: myapp-production
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgresql
    ports:
    - protocol: TCP
      port: 5432

---
# ✅ Allow DNS resolution
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: myapp-production
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: openshift-dns
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53

---
# ✅ Allow monitoring
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-monitoring
  namespace: myapp-production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: openshift-monitoring
    ports:
    - protocol: TCP
      port: 9090
```

## 12. **Operators y Custom Resources**

### 12.1 Custom Resource Definition
```yaml
# ✅ CRD para aplicación personalizada
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: myapps.example.com
spec:
  group: example.com
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              replicas:
                type: integer
                minimum: 1
                maximum: 100
              version:
                type: string
                pattern: '^v[0-9]+\.[0-9]+\.[0-9]+$'
              database:
                type: object
                properties:
                  enabled:
                    type: boolean
                  size:
                    type: string
                    enum: ["small", "medium", "large"]
            required:
            - replicas
            - version
          status:
            type: object
            properties:
              phase:
                type: string
                enum: ["Pending", "Running", "Failed"]
              message:
                type: string
  scope: Namespaced
  names:
    plural: myapps
    singular: myapp
    kind: MyApp
    shortNames:
    - ma

---
# ✅ Custom Resource instance
apiVersion: example.com/v1
kind: MyApp
metadata:
  name: myapp-prod
  namespace: myapp-production
spec:
  replicas: 5
  version: v1.2.0
  database:
    enabled: true
    size: large
```

## 13. **Troubleshooting y Debugging**

### 13.1 Comandos oc Específicos
```bash
# ✅ Información de cluster OpenShift
oc cluster-info
oc get clusterversion
oc get nodes -o wide

# ✅ Debugging de projects
oc get projects
oc describe project myapp-production
oc get all -n myapp-production

# ✅ Debugging de builds
oc get builds
oc logs bc/myapp -f
oc start-build myapp --follow

# ✅ Debugging de deployments
oc get dc
oc rollout status dc/myapp
oc rollout history dc/myapp
oc rollout undo dc/myapp

# ✅ Debugging de imagestreams
oc get is
oc describe is/myapp
oc tag myapp:latest myapp:backup

# ✅ Debugging de routes
oc get routes
oc describe route/myapp

# ✅ Port forwarding
oc port-forward pod/myapp-1-xyz 8080:8080
oc port-forward svc/myapp 8080:8080

# ✅ Remote shell
oc rsh deployment/myapp
oc exec -it pod/myapp-1-xyz -- /bin/bash

# ✅ Logs avanzados
oc logs -f dc/myapp --tail=100
oc logs --previous dc/myapp

# ✅ Debug de red
oc get svc,routes
oc get endpoints
```

### 13.2 Debug de Seguridad
```bash
# ✅ Verificar SCCs
oc get scc
oc describe scc restricted
oc adm policy who-can use scc restricted

# ✅ Verificar permisos
oc auth can-i create pods --as=system:serviceaccount:myapp:myapp-sa
oc describe rolebinding -n myapp-production

# ✅ Debug de ServiceAccount
oc get sa
oc describe sa myapp-sa
```

## 14. **Performance y Optimización**

### 14.1 Resource Tuning
```yaml
# ✅ HPA específico para OpenShift
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: myapp-production
spec:
  scaleTargetRef:
    apiVersion: apps.openshift.io/v1
    kind: DeploymentConfig
    name: myapp
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
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
        value: 100
        periodSeconds: 15
```

### 14.2 Node Affinity y Taints
```yaml
# ✅ Deployment con node affinity
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-compute-intensive
  namespace: myapp-production
spec:
  template:
    spec:
      # ✅ Node affinity para nodos específicos
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node-role.kubernetes.io/compute
                operator: In
                values:
                - "true"
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            preference:
              matchExpressions:
              - key: instance-type
                operator: In
                values:
                - c5.4xlarge
                - c5.9xlarge
        
        # ✅ Pod anti-affinity para distribución
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - myapp-compute-intensive
              topologyKey: kubernetes.io/hostname
      
      # ✅ Tolerations para taints
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "compute-intensive"
        effect: "NoSchedule"
      
      containers:
      - name: myapp
        # ... configuración del container
        resources:
          requests:
            cpu: 2000m
            memory: 4Gi
          limits:
            cpu: 4000m
            memory: 8Gi
```

---

## Checklist de Mejores Prácticas OpenShift

### ✅ Proyectos y Namespaces
- [ ] Usar Projects con metadata descriptiva
- [ ] Configurar ResourceQuotas y LimitRanges
- [ ] Implementar ProjectRequestTemplate personalizado
- [ ] Definir ownership y responsabilidades claras

### ✅ Seguridad
- [ ] Usar SCCs personalizados cuando sea necesario
- [ ] Implementar ServiceAccounts específicos
- [ ] Configurar Network Policies para microsegmentación
- [ ] Usar Service CA para certificados internos
- [ ] Nunca usar privileged containers

### ✅ Images y Builds
- [ ] Usar ImageStreams para gestión de imágenes
- [ ] Configurar BuildConfigs con triggers automáticos
- [ ] Implementar S2I cuando sea apropiado
- [ ] Usar Red Hat Universal Base Images (UBI)
- [ ] Configurar image scanning automático

### ✅ Deployments
- [ ] Considerar DeploymentConfig vs Deployment según necesidades
- [ ] Configurar health checks apropiados
- [ ] Implementar rolling deployment strategies
- [ ] Usar hooks de pre/post deployment cuando sea necesario

### ✅ Networking
- [ ] Usar Routes para exposición externa
- [ ] Configurar TLS termination apropiada
- [ ] Implementar rate limiting en Routes
- [ ] Usar Services para comunicación interna

### ✅ Storage
- [ ] Usar StorageClasses apropiados
- [ ] Configurar backup strategies
- [ ] Implementar StatefulSets para aplicaciones stateful
- [ ] Considerar data locality para performance

### ✅ CI/CD
- [ ] Implementar Tekton Pipelines
- [ ] Usar Triggers para webhooks automáticos
- [ ] Configurar security scanning en pipelines
- [ ] Implementar promotion entre entornos

### ✅ Monitoring
- [ ] Configurar ServiceMonitors para métricas
- [ ] Implementar PrometheusRules para alertas
- [ ] Configurar logging centralizado
- [ ] Usar dashboards de Grafana personalizados

## Recursos Adicionales

- [OpenShift Documentation](https://docs.openshift.com/)
- [Red Hat Developer Portal](https://developers.redhat.com/products/openshift)
- [OpenShift Blog](https://www.openshift.com/blog)
- [Tekton Documentation](https://tekton.dev/docs/)
- [OpenShift Container Platform Life Cycle Policy](https://access.redhat.com/support/policy/updates/openshift)

---

*Última actualización: Junio 2025*

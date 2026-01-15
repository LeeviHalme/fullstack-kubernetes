# fullstack-kubernetes

Repository for DevOps with Kubernetes -course organized by University of Helsinki in Fall 2025.

## Getting started

Creating a k3d cluster with 2 agents and exposing LB to port 80:

```
k3d cluster create k3s-default -p "80:80@loadbalancer" --agents 2
```

Applying configurations:

```
kubectl apply -f ./.../manifests/....yml
```

## Exercises

**Chapter 1:**

- [x] Exercise 0.1

**Chapter 2:**

- [Exercise 1.1](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.1/log-output)
- [Exercise 1.2](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.2/todo-app)
- [Exercise 1.3](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.3/log-output)
- [Exercise 1.4](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.4/todo-app)
- [Exercise 1.5](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.5/todo-app)
- [Exercise 1.6](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.6/todo-app)
- [Exercise 1.7](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.7/log-output)
- [Exercise 1.8](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.8/todo-app)
- [Exercise 1.9](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.9/pong-app)
- [Exercise 1.10](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.10/log-output)
- [Exercise 1.11](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.11/log-output)
- [Exercise 1.12](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.12/todo-app)
- [Exercise 1.13](https://github.com/LeeviHalme/fullstack-kubernetes/tree/1.13/todo-app)

**Chapter 3:**

- [Exercise 2.1](https://github.com/LeeviHalme/fullstack-kubernetes/tree/2.1/log-output)
- [Exercise 2.2](https://github.com/LeeviHalme/fullstack-kubernetes/tree/2.2/todo-backend)
- [Exercise 2.3](https://github.com/LeeviHalme/fullstack-kubernetes/tree/2.3/log-output)
- [Exercise 2.4](https://github.com/LeeviHalme/fullstack-kubernetes/tree/2.4/todo-app)
- [Exercise 2.5](https://github.com/LeeviHalme/fullstack-kubernetes/tree/2.5/log-output)
- [Exercise 2.6](https://github.com/LeeviHalme/fullstack-kubernetes/tree/2.6/todo-app)
- [Exercise 2.7](https://github.com/LeeviHalme/fullstack-kubernetes/tree/2.7/pong-app)
- [Exercise 2.8](https://github.com/LeeviHalme/fullstack-kubernetes/tree/2.8/todo-backend)
- [Exercise 2.9](https://github.com/LeeviHalme/fullstack-kubernetes/tree/2.9/todo-backend)
- [Exercise 2.10](https://github.com/LeeviHalme/fullstack-kubernetes/tree/2.10/todo-backend)

**Chapter 4:**

_No exercises completed_

**Chapter 5:**

- [Exercise 4.1](https://github.com/LeeviHalme/fullstack-kubernetes/tree/4.1/pong-app)
- Exercise 4.2
  - Prometheus query for the number of pods created by StatefulSets:
    ```
    sum(kube_pod_owner{namespace="prometheus", owner_kind="StatefulSet"})
    ```

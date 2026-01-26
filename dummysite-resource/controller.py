import requests
from kubernetes import client, config, watch

# Load cluster config
try:
    config.load_incluster_config()
except: # pylint: disable=bare-except
    config.load_kube_config()

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
custom_api = client.CustomObjectsApi()

def create_site_resources(name, namespace, url):
    """Create ConfigMap and Deployment for the dummy site."""
    print(f"Creating resources for {name} from {url}")

    # 1. Fetch the HTML
    try:
        html_content = requests.get(url, timeout=5).text
    except Exception as e: # pylint: disable=broad-except
        html_content = f"<html><body>Error fetching site: {e}</body></html>"

    # 2. Create ConfigMap to hold the HTML
    cm = client.V1ConfigMap(
        metadata=client.V1ObjectMeta(name=f"{name}-html"),
        data={"index.html": html_content}
    )
    v1.create_namespaced_config_map(namespace, cm)

    # 3. Create Nginx Deployment to serve the HTML
    dep = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=f"{name}-deploy"),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(match_labels={"app": name}),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": name}),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(
                        name="nginx",
                        image="nginx:alpine",
                        volume_mounts=[client.V1VolumeMount(
                            name="html-vol",
                            mount_path="/usr/share/nginx/html"
                        )]
                    )],
                    volumes=[client.V1Volume(
                        name="html-vol",
                        config_map=client.V1ConfigMapVolumeSource(name=f"{name}-html")
                    )]
                )
            )
        )
    )
    apps_v1.create_namespaced_deployment(namespace, dep)

def watch_dummy_sites():
    """Watch for DummySite CRD events and create resources."""
    w = watch.Watch()
    for event in w.stream(custom_api.list_cluster_custom_object, "stable.dwk", "v1", "dummysites"):
        obj = event['object']
        name = obj['metadata']['name']
        namespace = obj['metadata']['namespace']
        url = obj['spec']['website_url']

        if event['type'] == 'ADDED':
            create_site_resources(name, namespace, url)

if __name__ == "__main__":
    watch_dummy_sites()

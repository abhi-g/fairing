import json
from unittest.mock import patch

from kubernetes import client as k8s_client
from kubeflow.fairing.cloud.gcp import add_gcp_credentials_if_exists
from kubeflow.fairing.cloud.gcp import guess_project_name
from kubeflow.fairing.kubernetes.manager import KubeManager
from kubeflow.fairing.constants import constants


# Test guess_project_name with application default credentials.


def test_guess_project_name_application_default_file(tmp_path):
    creds_file = tmp_path / 'credentials'
    project_id = 'test_project'

    with creds_file.open('w') as f:
        json.dump({
            'project_id': project_id
        }, f)

    assert guess_project_name(str(creds_file)) == project_id

# Test that guess_project_name returns the project returned by
# google.auth.default when no input file is provided.


def test_guess_project_name_google_auth(tmp_path): #pylint:disable=unused-argument
    project_id = 'test_project'

    with patch('google.auth.default', return_value=(None, project_id)):
        assert guess_project_name() == project_id


def test_add_gcp_credentials_if_exists(tmp_path):
    pod_spec = k8s_client.V1PodTemplateSpec(
            metadata=k8s_client.V1ObjectMeta(name="fairing-deployer"))
    
    with patch('kubeflow.fairing.kubernetes.manager.KubeManager.secret_exists', return_value=False):
        add_gcp_credentials_if_exists(KubeManager(), pod_spec, 'kubeflow')
        assert pod_spec.service_account_name == constants.GCP_SERVICE_ACCOUNT_NAME

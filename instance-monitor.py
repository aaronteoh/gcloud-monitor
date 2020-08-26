# https://groups.google.com/g/gce-discussion/c/j4LIsIU6ne0?pli=1
# https://stackoverflow.com/questions/31343498/how-do-i-automatically-restart-a-gce-preemptible-instance
# https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances?hl=en_US

import os, pathlib
from logger import load_logger, logging


# https://cloud.google.com/compute/docs/regions-zones
# https://cloud.google.com/compute/docs/reference/rest/v1/instances/get
def get_instance(compute, project, zone, instance):
    result = compute.instances().get(project=project, zone=zone, instance=instance).execute()
    return result


# https://cloud.google.com/compute/docs/reference/rest/v1/instances/start
def start_instance(compute, project, zone, instance):
    request = compute.instances().start(project=project, zone=zone, instance=instance)
    response = request.execute()
    return response


if __name__ == '__main__':
    proj_dir = pathlib.Path(__file__).parent.absolute()
    filename = os.path.basename(__file__).split('.')[0]

    load_logger(proj_dir, filename)
    logging.debug('>>> Script start')

    try:
        # https://google-auth.readthedocs.io/en/latest/user-guide.html
        from google.oauth2 import service_account
        import googleapiclient.discovery
        import os, pathlib, json

        key_path = os.path.join(pathlib.Path(__file__).parent.absolute(), 'credentials','GOOGLE-CLOUD-CREDENTIALS.json')
        credentials = service_account.Credentials.from_service_account_file(key_path)

        # https://cloud.google.com/compute/docs/tutorials/python-guide
        # https://github.com/jeremyephron/simple-gmail/issues/6
        compute = googleapiclient.discovery.build('compute', 'v1', credentials=credentials, cache_discovery=False)

        with open(os.path.join(proj_dir, 'config/instances.json'), 'r') as f:
            config = json.load(f)

        for instance in config:
            project = config[instance]['project']
            zone = config[instance]['zone']

            status = get_instance(compute, project, zone, instance)['status']
            if status != 'RUNNING':
                logging.warning('%s / %s / %s STATUS: %s'%(project, instance, zone, status))
            # https://cloud.google.com/compute/docs/instances/instance-life-cycle
            # https://cloud.google.com/compute/docs/instances/preemptible
            if status == 'TERMINATED':
                response = start_instance(compute, project, zone, instance)
                logging.info(response)

    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
    else:
        logging.debug('Script complete')
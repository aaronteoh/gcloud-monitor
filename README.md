# gcloud-monitor
Monitor Google Cloud Compute Engine instances. Restart terminated instances.
<br><br>
1. Create small Compute Engine instance. **Ensure preemptability is turned off.** For free instance:
    - f1-micro instance (US regions only—excluding Northern Virginia [us-east4])
    - persistent disk <= 30 GB-months HDD
    - OS: Ubuntu
    - more details at https://cloud.google.com/free

2. SSH to instance

3. Configure timezone
    ```
    $ sudo ln -sf /usr/share/zoneinfo/Asia/Singapore /etc/localtime
    ```

4. Install python and pip

    ```
    $ sudo apt update
    $ sudo apt install python3
    $ sudo apt install python3-pip
    ```

5. Set up repo
    ```
    $ sudo mkdir /opt/repositories
    $ cd /opt/repositories
    $ sudo git clone https://github.com/aaronteoh/gcloud-monitor.git
   ```
   
6. Install dependancies
    ```
    $ cd /opt/gcloud-monitor
    $ sudo pip3 install -r requirements.txt
    ```
   
7. Create service account in GCP
    - ensure service account has access to view instance status and start instance 
    - download account key

8. Inside ssh, click on settings button, upload file, then upload key

9. Move key to credentials directory
    ```
    $ cd /home/$USER
    $ sudo mv <file name> /opt/repositories/streetcred/credentials/<file name>
    ```

10. Create config of instances to monitor
    ```
    $ echo '{"<instance name>": {"project": "<project name>", "zone": "<zone name>"}}' | sudo tee instances.json
    ```

11. Set up crontab
    ```
    $ sudo crontab /opt/repositories/gcloud-monitor/crontab
    ```
12. Test script
    ```
    $ cd /opt/repositories/gcloud-monitor
    $ sudo python3 instance-monitor.py
    ```
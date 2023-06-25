import cv2 as cv
import os
import requests
import json
import threading
from time import sleep
from sseclient import SSEClient
from typing import Dict, Any
import signal

class HWSystem:
    """
    Class representing a hardware system.
    """

    def __init__(self, access_key: str, base_route: str, sudo_pwd: str, register_json_path: str = 'register.json', config_json_path: str = 'config.json') -> None:
        """
        Initialize an instance of the HWSystem class.

        Args:
            access_key (str): The access key.
            base_route (str): The base route of the URL.
            sudo_pwd (str): The sudo password.
            register_json_path (str): The path to the register.json file.
            config_json_path (str): The path to the config.json file.
        """
        self.ACCESS_KEY = access_key
        self.BASE_ROUTE = base_route
        self.SUDO_PWD = sudo_pwd
        self.CONFIG_JSON = None
        self.sleep_time = 10
        self.registration_trials = 0
        self.register_json_path = register_json_path
        self.config_json_path = config_json_path
        
        self.RASPICAM_ID = 0
        self.OUTPUT_CHUNK_NAME = 'framechunk'
        self.SLEEP_BETWEEN_CHUNKS = 0 # seconds
        
        self.video_capturer = None
        self.video_writer = None
        
        with open(self.register_json_path) as register_data:
            self.REGISTER_JSON = json.load(register_data)
        self.REGISTER_JSON['access_key'] = self.ACCESS_KEY

        self.livestream_thread = None
        self.stop_livestream = threading.Event()

    def run_as_admin(self, cmd: str) -> None:
        """
        Run a sudo command.

        Args:
            cmd (str): The sudo command.
        """
        p = os.system('echo %s|sudo -S %s' % (self.SUDO_PWD, cmd))

    def write_json(self, json_entity: Dict[str, Any], file_name: str) -> None:
        """
        Write JSON data to a file.

        Args:
            json_entity (Dict[str, Any]): The JSON data to write.
            file_name (str): The name of the file.
        """
        
        if 'access_key' in json_entity:
            json_entity['access_key'] = ""
        
        json_object = json.dumps(json_entity)
        with open(file_name, "w") as out:
            out.write(json_object)

    def update_system(self) -> None:
        """
        Update the system by running 'apt-get update' and 'apt-get upgrade' commands.
        """
        self.run_as_admin('apt-get update -y')
        self.run_as_admin('apt-get upgrade -y')

    def handle_sse_remove(self) -> None:
        """
        Handle the 'RASP_REMOVE' event received through SSE.

        Removes the JSON configuration file and shuts down the module.
        """
        self.stop_livestream.set()
        print("[INFO] No longer livestreaming to the central server!")

        self.CONFIG_JSON = None
        os.remove(self.config_json_path)
        print("[INFO] The JSON Configuration file has been removed!")
        print("[INFO] The current module has been removed by the central server!")

        print("[GOODBYE] Shutting down...")

    def handle_sse_edit(self, event_data: Dict[str, Any]) -> None:
        """
        Handle the 'RASP_EDIT' event received through SSE.

        Updates the configuration JSON file based on the event data.

        Args:
            event_data (Dict[str, Any]): The data received in the SSE event.
        """
        if os.path.exists(self.register_json_path):
            os.remove(self.register_json_path)

        self.REGISTER_JSON['name'] = event_data['Camera Name']
        self.REGISTER_JSON['description'] = event_data['Camera Description']

        if event_data['Camera Preprocess']:
            if 'Preprocess' in event_data:
                self.CONFIG_JSON['Preprocess'] = event_data['Preprocess']

            if 'Utils' in event_data:
                self.CONFIG_JSON['Utils'] = event_data['Utils']
        else:
            if 'Preprocess' in self.CONFIG_JSON:
                del self.CONFIG_JSON['Preprocess']
            if 'Utils' in self.CONFIG_JSON:
                del self.CONFIG_JSON['Utils']

        print("[INFO] Successfully edited the configuration JSON!")
        self.REGISTER_JSON['preprocess_data'] = event_data['Camera Preprocess']

        self.write_json(self.REGISTER_JSON, self.register_json_path)
        print("[INFO] Successfully edited the registration JSON!")

        self.renew_config_json()

    def handle_sse_update(self) -> None:
        """
        Handle the 'RASP_UPDATE' event received through SSE.

        Sends a request to update the camera status to the central server.
        """
        self.stop_livestream.set()
        self.video_capturer.release()
        
        self.update_system()
        
        print('[INFO] Started livestreaming!')
        
        response = requests.get(f'{self.BASE_ROUTE}/api/camera/set-updated',
                                headers={'Authorization': 'Bearer ' + self.CONFIG_JSON['JWT Token']},
                                verify=True)
        self.renew_jwt_token(response.json())
        
        self.stop_livestream.clear()

    def handle_sse_start(self) -> None:
        """
        Handle the 'RASP_START' event received through SSE.

        Starts the livestream if it is not already running.
        """
        if self.livestream_thread.is_alive():
            print('[INFO] Already streaming...')
            return

        self.stop_livestream.clear()

        print('[INFO] Started livestreaming!')

    def handle_sse_stop(self) -> None:
        """
        Handle the 'RASP_STOP' event received through SSE.

        Stops the livestream.
        """
        self.stop_livestream.set()
        self.video_capturer.release()
        print('[INFO] Stopped livestreaming!')

    def listen_for_sse(self) -> None:
        """
        Listen for Server-Sent Events (SSE).
        """

        # Create an SSEClient instance to connect to the SSE endpoint
        client = SSEClient(f'{self.BASE_ROUTE}/stream')

        # Iterate over the events received from the SSE endpoint
        for event in client:
            event = json.loads(event.data)
            event_msg = event['message']
            event_data = json.loads(event['data'])

            print(f'[INFO] Catched event: {event_msg}')

            if not 'Camera ID' in event_data:
                print(f'[INFO] Ignored event: {event_msg}')
                return

            event_camera_id = event_data['Camera ID']
            if event_camera_id != self.CONFIG_JSON['Camera ID']:
                print("[INFO] The event is not directed to this device! ")
                print("[INFO] Ignoring event...")
                continue

            if event_msg == 'RASP_REMOVE':
                self.handle_sse_remove()
                return
            elif event_msg == 'RASP_EDIT':
                self.handle_sse_edit(event_data)
            elif event_msg == 'RASP_UPDATE':
                self.handle_sse_update()
            elif event_msg == 'RASP_START':
                self.handle_sse_start()
                self.start_module()
            elif event_msg == 'RASP_STOP':
                self.handle_sse_stop()

    def attempt_registration(self) -> bool:
        """
        Attempt to register with the central server.

        Returns:
            bool: True if the registration is successful, False otherwise.
        """

        while True:
            if self.registration_trials >= 10:
                print("Too many attempts without any success.")
                print("Stopping...")
                return False

            print("Attempting registration to the central server...")
            response = self.register()

            if response['Code'] == 200:
                print("[SUCCESS] Registration successful!")
                print("Saving registration data to local JSON file...")

                self.JWT_KEY = response['Data']['JWT Token']
                self.CAMERA_ID = response['Data']['Camera ID']

                self.write_json(response, self.config_json_path)

                print("[SUCCESS] Successfully saved registration data to local JSON file!")
                break
            elif response['Code'] == 403:
                print("[FAIL] Registration failed!")
                print("Reason: The ACCESS KEY is incorrect.")

                if self.registration_trials > 0:
                    print("Please review the current ACCESS KEY")
                    return False
                print("Trying one more time...")
                self.registration_trials += 1
            else:
                print("[FAIL] Registration failed for an unknown reason!")
                print(f'Sleeping for {self.sleep_time} seconds!')
                self.registration_trials += 1
                sleep(self.sleep_time * self.registration_trials)

        return True

    def renew_config_json(self) -> None:
        """
        Renew the configuration JSON file by updating it with the current configuration data.
        """
        with open(self.config_json_path, 'r') as config:
            INITIAL_CONFIG_JSON = json.load(config)
            INITIAL_CONFIG_JSON['Data'] = self.CONFIG_JSON
            self.write_json(INITIAL_CONFIG_JSON, self.config_json_path)

    def renew_jwt_token(self, response_json: Dict[str, Any]) -> None:
        """
        Renew the JWT token by updating it with the new token obtained from the response.

        Args:
            response_json (Dict[str, Any]): The JSON response from the server.
        """
        jwt_token = response_json

        if 'Data' in jwt_token:
            jwt_token = jwt_token['Data']

        if 'JWT Token' in jwt_token:
            jwt_token = jwt_token['JWT Token']

        self.CONFIG_JSON['JWT Token'] = jwt_token
        self.renew_config_json()

        print('[SUCCESS] Renewed JWT Token!')

    def record_chunk(self) -> None:
        i = 0
        
        output_file_name = self.OUTPUT_CHUNK_NAME + '.' + self.CONFIG_JSON['Preprocess']['DataFormat']
        
        FRAME_WIDTH = int(self.video_capturer.get(cv.CAP_PROP_FRAME_WIDTH))
        FRAME_HEIGHT = int(self.video_capturer.get(cv.CAP_PROP_FRAME_HEIGHT))
        
        # VideoWriter object to save the recorded video.
        self.video_writer = cv.VideoWriter(output_file_name,
                             cv.VideoWriter_fourcc(*'mp4v'), 
                             self.CONFIG_JSON['Preprocess']['ChunkSize'],
                             (360, 360))
                             
        while True:
            # Read a frame from the camera.
            ret, frame = self.video_capturer.read()
            
            # Check if the frame has been successfully read.
            if not ret:
                print('[ERROR] Failed to read the frame!')
                print('Aborting...')
                return
                
            resized_frame = cv.resize(frame, (360, 360))
                
            # Write the frame to the output video.
            self.video_writer.write(resized_frame) 
            
            # Exit the loop if 'q' is pressed.
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
                
            i += 1
            if i >= self.CONFIG_JSON['Preprocess']['ChunkSize']:
                break
                
        self.video_writer.release()
        
        
    def livestream(self) -> None:
        """
        Perform the livestreaming to the central server.
        """
        output_file_name = self.OUTPUT_CHUNK_NAME + '.' + self.CONFIG_JSON['Preprocess']['DataFormat']
        
        while not self.stop_livestream.is_set():
            print('[INFO] Livestreaming to the central server...')
            self.record_chunk()
            
            with open(output_file_name, 'rb') as f:
                
                try: 
                    response = requests.post(f'{self.BASE_ROUTE}/api/send/frames',
                                                files={output_file_name: f},
                                                headers={'Authorization': 'Bearer ' + self.CONFIG_JSON['JWT Token']})
                    response_json = response.json()
                except:
                    raise requests.exceptions.ConnectionError()
                        
            if 'Code' not in response_json:
                self.video_capturer.release()
                raise requests.exceptions.ConnectionError()
            
            if response_json['Code'] == 400:
                self.handle_sse_stop()
                return
            elif response_json['Code'] == 403:
                if os.path.exists(self.config_json_path):
                    os.remove(self.config_json_path)
            
            # Renewing the JWT Token
            self.renew_jwt_token(response.json())
            
            sleep(self.SLEEP_BETWEEN_CHUNKS)
            
        self.video_capturer.release()

    def start_module(self) -> None:
        """
        Start the Raspberry PI module.
        """
        while True:
            try:
                print("[START] Raspberry PI module...")
                
                # Open the video capture.
                self.video_capturer = cv.VideoCapture(self.RASPICAM_ID)

                # Check if the camera has ben successfully opened.
                if not self.video_capturer.isOpened():
                        print('[ERROR] Failed to open the camera!')
                        print('Aborting...')
                        exit(1)
                
        
                register_is_success = None
                if not os.path.exists(self.config_json_path):
                    register_is_success = self.attempt_registration()

                    if not register_is_success:
                        return

                with open(self.config_json_path) as config_data:
                    self.CONFIG_JSON = json.load(config_data)
                    self.CONFIG_JSON = self.CONFIG_JSON['Data']

                self.livestream_thread = threading.Thread(target=self.livestream)
                
                # Starting the livestream session on a separate thread.
                self.livestream_thread.start()
                              
                # Listening for SSEs on the current thread.
                self.listen_for_sse()

                self.livestream_thread.join()
                
                
            except requests.exceptions.ConnectionError:
                if self.livestream_thread.is_alive():
                    self.livestream_thread.join()
                
                self.video_capturer.release()
                
                print('[ERROR] Connection error! Aborting...')
                exit(1)

            sleep(5)

    def register(self) -> Dict[str, Any]:
        """
        Register the camera with the central server.

        Returns:
            Dict[str, Any]: The JSON response from the server.
        """
        response = requests.post(f'{self.BASE_ROUTE}/api/camera/register',
                                 json=self.REGISTER_JSON,
                                 verify=True)

        return response.json()

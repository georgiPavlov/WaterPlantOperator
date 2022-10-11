import socket
import logging
import http as h
import requests
import run.common.json_creator as jc
import run.common.file as f
from run.operation.camera_op import CAMERA_FORMAT
import os


class IServerCommunicatorInterface:

    # getPlan
    def get_plan(self):
        pass

    # postWaterpip index versions
    def post_water(self, water):
        pass

    # postMoisture
    def post_moisture(self, moisture_level):
        pass

    # postPicture
    def post_picture(self, photo_name):
        pass

    # postPlanExecution
    def post_plan_execution(self, status):
        pass

    # getWaterLevel
    def get_water_level(self, status):
        pass


class ServerCommunicator(IServerCommunicatorInterface):
    GET_PLAN_URL = 'getPlan'
    POST_WATER_URL = 'postWater'
    POST_MOISTURE_URL = 'postMoisture'
    POST_PICTURE = 'postPhoto'
    GET_PICTURE = 'getPhoto'
    POST_STATUS = 'postStatus'
    GET_WATER = 'getWaterLevel'
    IMAGE_PATH = '/tmp/image.png'
    APP_MASTER_URL = 'gadget_communicator_pull'
    PROTOCOL = 'http'
    PORT = '8080'
    IP_ADDRESS = 'water-me-lb-842691727.eu-central-1.elb.amazonaws.com'

    def __init__(self, device_guid, photos_dir):
        self.device_guid = device_guid
        self.water_server_ip = self.get_ip_address()
        self.photos_dir = photos_dir
        IServerCommunicatorInterface.__init__(self)

    def get_plan(self):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.water_server_ip, self.GET_PLAN_URL)
        device_json = {'device': self.device_guid}
        response = None
        payload = ""
        try:
            response = requests.get(request_url, data=payload, params=device_json)
            logging.info(response.url)
            if response.status_code == h.HTTPStatus.NO_CONTENT:
                logging.info(f'No new plan in queue: {response.status_code}')
            elif response.status_code == h.HTTPStatus.FORBIDDEN:
                logging.info(f'Device not registered: {response.status_code}')
            elif response.status_code == h.HTTPStatus.OK:
                logging.info(f'New plan found: {response.status_code}')
                json_response = response.json()
                logging.info(f'Response: {json_response}')
                return json_response
            else:
                logging.info(f'response: {response.status_code}')
        except requests.exceptions.RequestException as e:
            logging.info(f'exception with server {str(e)}')
            self.print_respose(response)
        return self.return_emply_json()

    def print_respose(self, response):
        if response is not None:
            logging.info(response.text)

    def post_water(self, water_level):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.water_server_ip, self.POST_WATER_URL)
        payload = {'device': self.device_guid, 'water_level': water_level}
        headers = {"Content-Type": "application/json"}
        response = None
        try:
            response = requests.request("POST", request_url, json=payload, headers=headers)
            logging.info(response.url)
            if response.status_code == h.HTTPStatus.FORBIDDEN:
                logging.info(f'Device not registered: {response.status_code}')
            elif response.status_code == h.HTTPStatus.CREATED:
                logging.info(f'Water posted: {response.status_code}')
                json_response = response.json()
                return json_response
            else:
                logging.info(f'response: {response.status_code}')
        except requests.exceptions.RequestException as e:
            logging.info(f'exception with server {str(e)}')
            self.print_respose(response)
        return self.return_emply_json()

    def post_moisture(self, moisture_level):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.water_server_ip, self.POST_MOISTURE_URL)
        payload = {'device': self.device_guid, 'moisture_level': moisture_level}
        headers = {"Content-Type": "application/json"}
        response = None
        try:
            response = requests.request("POST", request_url, json=payload, headers=headers)
            logging.info(response.url)
            if response.status_code == h.HTTPStatus.FORBIDDEN:
                logging.info(f'Device not registered: {response.status_code}')
            elif response.status_code == h.HTTPStatus.CREATED:
                logging.info(f'Moisture level posted: {response.status_code}')
                json_response = response.json()
                return json_response
            else:
                logging.info(f'response: {response.status_code}')
        except requests.exceptions.RequestException as e:
            logging.info(f'exception with server {str(e)}')
            self.print_respose(response)
        return self.return_emply_json()

    def post_picture(self, photo_name):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.water_server_ip, self.POST_PICTURE)
        photo_path = f'{self.photos_dir}/{photo_name}{CAMERA_FORMAT}'

        try:
            os.system(f"curl --request POST \
              --url {request_url} \
              --header 'Content-Type: multipart/form-data; boundary=---011000010111000001101001' \
              --form image_file=@{photo_path} \
              --form device_id={self.device_guid} \
              --form photo_id={photo_name}")
        except requests.exceptions.RequestException as e:
            logging.info(f'exception with server {str(e)}')

    def get_picture(self):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.water_server_ip, self.GET_PICTURE)
        device_json = {'device': self.device_guid}
        response = None
        try:
            response = requests.get(request_url, params=device_json)
            logging.info(response.url)
            if response.status_code == h.HTTPStatus.NO_CONTENT:
                logging.info(f'No new picture in queue: {response.status_code}')
            elif response.status_code == h.HTTPStatus.FORBIDDEN:
                logging.info(f'Device not registered: {response.status_code}')
            elif response.status_code == h.HTTPStatus.OK:
                logging.info(f'New picture for capture: {response.status_code}')
                json_response = response.json()
                logging.info(f'Response: {json_response}')
                return json_response
            else:
                logging.info(f'response: {response.status_code}')
        except requests.exceptions.RequestException as e:
            logging.info(f'exception with server {str(e)}')
            self.print_respose(response)
        return self.return_emply_json()

    def post_plan_execution(self, status):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.water_server_ip, self.POST_STATUS)
        payload = {'device': self.device_guid, 'execution_status': status.watering_status, 'message': status.message}
        headers = {"Content-Type": "application/json"}
        response = None
        try:
            response = requests.request("POST", request_url, json=payload, headers=headers)
            logging.info(response.url)
            if response.status_code == h.HTTPStatus.FORBIDDEN:
                logging.info(f'Device not registered: {response.status_code}')
            elif response.status_code == h.HTTPStatus.CREATED:
                logging.info(f'Status posted: {response.status_code}')
                json_response = response.json()
                return json_response
            else:
                logging.info(f'response: {response.status_code}')
        except requests.exceptions.RequestException as e:
            logging.info(f'exception with server {str(e)}')
            self.print_respose(response)
        return self.return_emply_json()

    def get_water_level(self):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.water_server_ip, self.GET_WATER)
        device_json = {'device': self.device_guid}
        response = None
        try:
            response = requests.get(request_url, params=device_json)
            logging.info(response.url)
            if response.status_code == h.HTTPStatus.NO_CONTENT:
                logging.info(f'No water reset in queue: {response.status_code}')
            elif response.status_code == h.HTTPStatus.FORBIDDEN:
                logging.info(f'Device not registered: {response.status_code}')
            elif response.status_code == h.HTTPStatus.OK:
                logging.info(f'Reset water: {response.status_code}')
                json_response = response.json()
                logging.info(f'Response: {json_response}')
                return json_response
            else:
                logging.info(f'response: {response.status_code}')
        except requests.exceptions.RequestException as e:
            logging.info(f'exception with server {str(e)}')
            self.print_respose(response)
        return self.return_emply_json()

    def print_respose(self, response):
        if response is not None:
            logging.info(response.text)

    # to do revert to constant usage when using real ip address
    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        logging.info(f'ip address: {ip_address}')
        s.close()
        return self.IP_ADDRESS

    def build_ulr_for_request(self, protocol, ip, request_url):
        url_address = f'{protocol}://{ip}:{self.PORT}/{self.APP_MASTER_URL}/{request_url}'
        logging.info(f'url_address: {url_address}')
        return url_address

    def return_emply_json(self):
        return jc.get_json("{}")

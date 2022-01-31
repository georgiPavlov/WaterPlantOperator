import socket
from http import HTTPStatus
import requests
import run.common.json_creator as jc
import run.common.file as f


class IServerCommunicatorInterface:

    #getPlan
    def get_plan(self):
        pass

    #postWater
    def post_water(self, water):
        pass

    #postMoisture
    def post_moisture(self, moisture_level):
        pass

    #postPicture
    def post_picture(self):
        pass
    
    #postPlanExecution
    def post_plan_execution(self, status):
        pass


class ServerCommunicator(IServerCommunicatorInterface):
    GET_PLAN_URL = 'getPlan'
    POST_WATER_URL = 'postWater'
    POST_MOISTURE_URL = 'postMoisture'
    POST_PICTURE = 'postPicture'
    POST_STATUS = 'postStatus'
    IMAGE_PATH = '/tmp/image.png'
    PROTOCOL = 'http'
    #device_guid = 'ab313658-5d84-47d6-a3f1-b609c0f1dd5e'

    def __init__(self, device_guid):
        self.device_guid = device_guid
        IServerCommunicatorInterface.__init__(self)

    def get_plan(self):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.get_ip_address, self.GET_PLAN_URL)
        device_json = {'device': self.device_guid}
        response = None
        try:
            response = requests.get(request_url, params=device_json)
            print(response.url)
            if response.status_code == HTTPStatus.NO_CONTENT:
                print(f'No new plan in queue: {response.status_code}')
            elif response.status_code == HTTPStatus.FORBIDDEN:
                print(f'Device not registered: {response.status_code}')
            elif response.status_code == HTTPStatus.OK:
                print(f'New plan found: {response.status_code}')
                json_response = response.json()
                return json_response
            else:
                print(f'response: {response.status_code}')
        except requests.exceptions.RequestException:
            print(response.text)
        return self.return_emply_json()

    def post_water(self, water_level):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.get_ip_address, self.POST_WATER_URL)
        device_json = {'device': self.device_guid, 'water_level': water_level}
        response = None
        try:
            response = requests.post(request_url, data=device_json)
            print(response.url)
            if response.status_code == HTTPStatus.FORBIDDEN:
                print(f'Device not registered: {response.status_code}')
            elif response.status_code == HTTPStatus.CREATED:
                print(f'Water posted: {response.status_code}')
                json_response = response.json()
                return json_response
            else:
                print(f'response: {response.status_code}')
        except requests.exceptions.RequestException:
            print(response.text)
        return self.return_emply_json()

    def post_moisture(self, moisture_level):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.get_ip_address, self.POST_MOISTURE_URL)
        device_json = {'device': self.device_guid, 'moisture_level': moisture_level}
        response = None
        try:
            response = requests.post(request_url, data=device_json)
            print(response.url)
            if response.status_code == HTTPStatus.FORBIDDEN:
                print(f'Device not registered: {response.status_code}')
            elif response.status_code == HTTPStatus.CREATED:
                print(f'Moisture level posted: {response.status_code}')
                json_response = response.json()
                return json_response
            else:
                print(f'response: {response.status_code}')
        except requests.exceptions.RequestException:
            print(response.text)
        return self.return_emply_json()

    def post_picture(self):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.get_ip_address, self.POST_PICTURE)
        base64_image = f.return_file_content_in_base64_format(self.IMAGE_PATH)

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = jc.dump_json({"image": base64_image, "other_key": "value"})
        response = None
        try:
            response = requests.post(request_url, data=payload, headers=headers)
            data = response.json()
            print(data)
        except requests.exceptions.RequestException:
            print(response.text)
            
    def post_plan_execution(self, status):
        request_url = self.build_ulr_for_request(self.PROTOCOL, self.get_ip_address, self.POST_STATUS)
        device_json = {'device': self.device_guid, 'execution_status': status.execution_status, 'message': status.message}
        response = None
        try:
            response = requests.post(request_url, data=device_json)
            print(response.url)
            if response.status_code == HTTPStatus.FORBIDDEN:
                print(f'Device not registered: {response.status_code}')
            elif response.status_code == HTTPStatus.CREATED:
                print(f'Status posted: {response.status_code}')
                json_response = response.json()
                return json_response
            else:
                print(f'response: {response.status_code}')
        except requests.exceptions.RequestException:
            print(response.text)
        return self.return_emply_json()

    # to do revert to constant usage when using real ip address
    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        print(f'ip address: {ip_address}')
        s.close()
        return ip_address

    def build_ulr_for_request(self, protocol, ip, request_url):
        url_address = f'{protocol}://{ip}/{request_url}'
        print(f'url_address: {url_address}')
        return url_address

    def return_emply_json(self):
        return jc.get_json("{}")

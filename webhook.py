"""
This file use for filter event when  webhook activated
it must deployed on backend
Event type detail show in
        --- https://dev.netatmo.com/en-US/resources/technical/reference/cameras#event

"""
import requests
import json


class API :
    def __init__(self, **kwargs):
        # Initialized common attributes
        self.variables = kwargs

    # These set and get methods allow scalability
    def set_variable(self, k, v):  # k=key, v=value
        self.variables[k] = v

    def get_variable(self, k):
        return self.variables.get(k, None)  # default of get_variable is none

    def get_access_token(self):
        # Request Netatmo
        # POST https://api.netatmo.com/oauth2/token
        try:
            response = requests.post(
                url="https://api.netatmo.com/oauth2/token",
                headers={
                    "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
                },
                data={
                    "client_id":"5a8ab6e43164802f5f8b49fe",
                    "username":"peahive@gmail.com",
                    "password":"28Sep1960",
                    "scope":"read_camera",
                    "client_secret":"eFtLEV6Fe3rt3AdAdBM7fJQL0gwCfNWSYmxwysWsTEL3v",
                    "grant_type":"password",
                },
            )
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            return json.loads(response.content)

        except requests.exceptions.RequestException:
            print('HTTP Request failed')


def movement_event(input):
    print('movement detected')
    # do something for movement detected


def people_event(input):
    print('people detected')
    # do something for people detected
    person =input.get('persons') # person from return response with face_id key
    home_id = input.get('home_id')
    netatmo = API().get_access_token()
    access_token = netatmo.get('access_token')
    for ind in range(len(person)):
        if dict(person[ind]).get('is_known') :
            print('Got Known Person Seen')
            face_id = person[ind].get('face_id')
            try:
                response = requests.get(
                    url="https://api.netatmo.net/api/gethomedata", # Request for person id list
                    params={
                        "access_token": access_token,
                        "home_id": home_id,
                        "size":"2", # Retrive 2 event in response
                    },
                )
                print('Response HTTP Status Code: {status_code}'.format(
                    status_code=response.status_code))
                data = json.loads(response.content)
                data = data.get('body')
                homes = data['homes']
                #TODO : Try to get person or face id only known person and matching
                #TODO : to find who are arrive home
                for ind in range(len(homes)):
                    person_list = homes[ind].get('persons')
                    for id in person_list:
                        if face_id == id.get('faces').get('id') :
                            print('Matched Person')
                            person_name = id.get('pseudo')
                            #TODO : do something for trigger this person arrive home

            except requests.exceptions.RequestException:
                print('HTTP Request failed')

        else:
            print('Got Unknown Person Seen') # Unknown person trigger
            #TODO : do something for unknown person seen --> get picture of them
            face_id = dict(person[ind]).get('face_id')
            face_key = dict(person[ind]).get('face_key')
            # request for picture of person
            try:
                response = requests.get(
                    url="https://api.netatmo.com/api/getcamerapicture",
                    params={
                        "access_token": access_token,
                        "image_id": face_id,
                        "key": face_key,
                    },
                )
                print('Response HTTP Status Code: {status_code}'.format(
                    status_code=response.status_code))
                print('Response HTTP Response Body: {content}'.format(
                    content=response.content)) # Response.content that contain only byte data of picture

            except requests.exceptions.RequestException:
                print('HTTP Request failed')


def get_event_type(data):
    print('decoding event type')
    try:
        if data.has_key('event_type'):
            event_type = data.get('event_type')
            if event_type == 'movement' :
                # do something for event movement
                print('Movement Trigger')
                movement_event(data)

            elif event_type == 'person' :
                print('People seen Trigger')
                people_event(data)

    except Exception as Error:
        print(Error)


def main():
    print('Server Listening ...')
    res = { 'user_id': '59e43899b26ddf6c058ba402',
                       'app_type': 'app_camera','event_type': 'movement',
                       'camera_id': '70:ee:50:18:78:0e','home_id': '5a62cbd62b2b4684478ba52a',
                       'home_name': 'PEA Smart Home','message': 'Motion detected'}
                       # res variable is a simmulate data for incoming msg when event trigger on webhook
    # something from netatmo webhook  and decode into json fromat
    print('Data Hooked')
    get_event_type(res)


if __name__ == '__main__':
    main()

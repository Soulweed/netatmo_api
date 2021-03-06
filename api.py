import requests
import json


def push2db(persons):
    print('Start Connect to database')
    return True


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
            # TODO : Important - change data parameter for a new netatmo
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

    # def send_request(self):
    #     # Get Home Data
    #     # GET https://api.netatmo.net/api/gethomedata
    #
    #     try:
    #         response = requests.get(
    #                 url="https://api.netatmo.net/api/gethomedata",
    #                 params={
    #                     "access_token":"59e43899b26ddf6c058ba402|f7668750f6799334ace90f576df0666d",
    #                 },
    #         )
    #         print('Response HTTP Status Code: {status_code}'.format(
    #                 status_code=response.status_code))
    #         print('Response HTTP Response Body: {content}'.format(
    #                 content=response.content))
    #     except requests.exceptions.RequestException:
    #         print('HTTP Request failed')

    def get_home_data(self,k):
        print('Get home data API')
        # Get Home Data
        # GET https://api.netatmo.net/api/gethomedata

        try:
            response = requests.get(
                url="https://api.netatmo.net/api/gethomedata",
                params={
                    "access_token":str(k),
                },
            )
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            temp = json.loads(response.content)
            persons =((temp.get('body')).get('homes')[0]).get('persons')
            persons_list = []
            for ind in range(len(persons)):
                if persons[ind].has_key('pseudo'):
                    # print('------------------------------------------------')
                    # print('Name     : '+(persons[ind].get('pseudo')).encode('utf-8','unicode')) # Some pseudo is invalid format
                    # print('Face ID  : '+str((persons[ind].get('face')).get('id')))
                    # print('Face Key : '+str((persons[ind].get('face')).get('key')))
                    # print('------------------------------------------------')
                    persons_list.append(persons[ind])
                    if persons[ind].get('out_of_sight') == False:
                        print((persons[ind].get('pseudo')).encode('utf-8','unicode')+" at home")

            # TODO : Add Known people from netatmo welcome to Database
            flag = push2db(persons_list)

            if flag :

                print('Updatae Database Successful')

            else:

                print('Update Database Failure')


            return persons
        except requests.exceptions.RequestException:
            print('HTTP Request failed')



def main():

    netatmo = API()
    # netatmo.send_request()
    content = netatmo.get_access_token()
    access_token = content.get('access_token')
    refresh_token = content.get('refresh_token')
    home_data = netatmo.get_home_data(access_token)
    print(home_data)

if __name__ == '__main__':
    main()
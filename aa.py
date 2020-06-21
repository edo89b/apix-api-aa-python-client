#importo librearie
import requests
import base64
import json
import platform
import hashlib
import datetime
import sys

#Costanti programma
API_URL = 'https://aa.nextog.cloud/'
API_CLIENT_VERSION = '1.0.8beta'
API_CLIENT_PLATFORM = platform.system()+':'+platform.version()+';Python:'+platform.python_version()

class ApixAPI:
    #Dochiarazione attributi
    ApiSessionToken = ''
    UserSessionToken = ''
    
    # Inizializzo API
    def __init__(self,auto_login=True):
        if(auto_login):
            output = self.SendRequest('api/login')
            
            #Imposto l'API Session ID, da utilizzare per le future richieste all'interno di questa istanza
            self.ApiSessionToken = output.get('api-session-token')
        
    #Decode base64 string
    def base64_decode(self,string):
        if(string):
            return base64.b64decode(string).decode("utf-8") 
    
    #HASH MD5
    def md5(self,string):
        return hashlib.md5(string.encode()).hexdigest()

    #Verifico se la richiesta ha restituito un error
    def CheckError(self,output):
        for x in output:
            if(x=='status' and output[x]=='error'):
                error_message = 'ERROR ['+str(output['error_no'])+']: '+output['message']
                if(output['error_no']==7):
                    sys.exit(error_message)
                else:
                    print(error_message)
                
    #Creazione Api Session Token Dinamico
    def CreateDynamicApiSessionToken(self,token):
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.md5(token+datetime_str).upper()
    
    #Invio richiesta al server
    def SendRequest(self,cmd,data={}):  
    
        data.update({'api-client-version':API_CLIENT_VERSION,'api-client-platform':API_CLIENT_PLATFORM})
        
        headers = {}
        if(self.ApiSessionToken):
            headers.update({'api-session-token': self.CreateDynamicApiSessionToken(self.ApiSessionToken)})
            
        if(self.UserSessionToken):
            headers.update({'user-session-token': self.UserSessionToken})
        
        try:
            r = requests.post(API_URL+"/"+cmd, data=data, headers=headers)
        except requests.exceptions.HTTPError as errh:
            sys.exit("ERROR: Http: "+errh)
        except requests.exceptions.ConnectionError:
            sys.exit('ERROR: Connection failed to url '+API_URL)
        except requests.exceptions.Timeout as errt:
            sys.exit("ERROR: Timeout: "+errt)
        except requests.exceptions.RequestException as err:
            sys.exit("ERROR: Something Else: "+err)

        try:
            output = json.loads(self.base64_decode(r.text))
        except ValueError:
            if(r.text):
                print(r.text)
                ##print('WARNING: Command "'+cmd+'" not found')
                output = {'status':'error','message':'Command "'+cmd+'" not found','error_no':8}
            else:
                sys.exit('ERROR: Decoding JSON has failed')
            
        #Verifico se è presente un errore nella richiesta
        self.CheckError(output)
        
        return output
        
    #def __del__(self):
    #    requests.post(API_URL+"/echo")
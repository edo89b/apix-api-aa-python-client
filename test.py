#Importo libreria apix
from aa import *
import sys

print('## INIZIALIZZO LE API')
API = ApixAPI(False)

print('\r\n## INVIO IL COMANDO DI LOGIN API "api/login"')
output = API.SendRequest('api/login')
print(output)
API.ApiSessionToken = output.get('api-session-token')
print('\r\n## SESSION-TOKEN: '+API.ApiSessionToken)

print('\r\n## INIZIALIZZO LE API INVIANDO IL COMANDO "debug/echo" CHE MI RESTITUIRà I PARAMETRI INVIATI TRAMITE POST')
output = API.SendRequest('debug/echo',{'test1':'prova1 con token'})
print(output)

print('\r\n## INIZIALIZZO LE API INVIANDO IL COMANDO CHE NON ESISTE "debug/echo2" CHE MI RESTITUIRà UN ERRORE')
output = API.SendRequest('debug/echo2',{'test2':'prova1 comando che non esiste'})
print(output)

print('\r\n## REINVIO ERRONAMENTE IL COMANDO "api/login", MI VERRà RESISTUITO UN ERRORE')
output = API.SendRequest('api/login')
print(output)

print('\r\n## INVIO IL COMANDO "debug/random"')
output = API.SendRequest('debug/random')
print(output)

print('\r\n## INVIO IL COMANDO "info/server"')
output = API.SendRequest('info/server')
print(output)

#LOGOUT UTENTE
"""
print('\r\n## LOGOUT UTENTE CON UTENTE NON AUTENTICATO')
output = API.SendRequest('logout')
print(output)
"""


# AUTENTICAZIONE UTENTE 
print('\r\n## AUTENTICAZIONE UTENTE')
while True:
    
    username = input('Username: ')
    password = API.md5(input('Passowrd: '))
    
    print('## HASH MD5 della password '+password)
    output = API.SendRequest('user/login',{'username':username,'password':password})
    print(output)
    
    if(output.get('status')=='error' and output.get('error_no')==99999):
        sys.exit();
    elif(output.get('status')=='success' and not output.get('authenticator')):
        break
    elif(output.get('status')=='success' and output.get('authenticator')):
        while True:
            otp = input('Inserisci cdice OTP: ')
            print('## INVIO SECONDA RICHIESTA DI LOGIN CON CODICE OTP')
            output = API.SendRequest('user/login',{'username':username,'password':password,'otp':otp})
            print(output)
            
            if(output.get('status')=='error' and output.get('error_no')==99999):
                sys.exit();
            elif(output.get('status')=='success'):
                break
        break
    elif(output.get('status')=='error' and output.get('error_no')!=2):
        break
        
    
        
print('\r\n## IMPOSTO TOKEN UTENTE') 
API.UserSessionToken = output.get('user-session-token')
print('\r\n## USER-TOKEN: '+API.UserSessionToken)   
# FINE AUTENTICAZIONE UTENTE

# RICHIESTA INFORMAZIONI UTENTE
print('\r\n## RICHIESTA INFORMAZIONI UTENTE')
output = API.SendRequest('user/info')
print(output)

# RICHIESTA ELENCO AZIENDE UTENTE
print('\r\n## RICHIESTA ELENCO AZIENDE UTENTE')
output = API.SendRequest('user/companies')
print(output)

# RICHIESTA ELENCO APPLICAZIONI
print('\r\n## RICHIESTA ELENCO APPLICAZIONI')
output = API.SendRequest('user/apps_t2')
print(output)

# RICHIESTA INFORMAZIONI APPLICAZIONE
print('\r\n## RICHIESTA INFORMAZIONI APPLICAZIONE')
output = API.SendRequest('app_t2/info',{'name':'gestione_malattia'})
print(output)

# RICHIESTA INFORMAZIONI APPLICAZIONE SENZA FILE JSON
print('\r\n## RICHIESTA INFORMAZIONI APPLICAZIONE articoli')
output = API.SendRequest('app_t2/info',{'name':'articoli'})
print(output)

# RICHIESTA INFORMAZIONI APPLICAZIONE SENZA FILE JSON
print('\r\n## RICHIESTA INFORMAZIONI APPLICAZIONE SENZA FILE JSON')
output = API.SendRequest('app_t2/info',{'name':'articoli_parent'})
print(output)

# RICHIESTA INFORMAZIONI APPLICAZIONE CHE NON ESISTE
print('\r\n## RICHIESTA INFORMAZIONI APPLICAZIONE CHE NON ESISTE')
output = API.SendRequest('app_t2/info',{'name':'app_che_non_esiste'})
print(output)

# ESEGUO COMANDO CHE GENERA UN ERRORE DELLA QUERY
print('\r\n## ESEGUO COMANDO CHE GENERA UN ERRORE DELLA QUERY')
output = API.SendRequest('debug/query_error')
print(output)

# IMPOSTO UN AZIENDA ATTIVA CHE NON ESISTE
print('\r\n## IMPOSTO UN AZIENDA ATTIVA CHE NON ESISTE')
output = API.SendRequest('user/set_company',{'id_azienda':'300'})
print(output)

# IMPOSTO UN AZIENDA ATTIVA CHE ESISTE
print('\r\n## IMPOSTO UN AZIENDA ATTIVA CHE ESISTE')
output = API.SendRequest('user/set_company',{'id_azienda':'2'})
print(output)

# RICHIESTA ELENCO APPLICAZIONI
print('\r\n## RICHIESTA ELENCO APPLICAZIONI')
output = API.SendRequest('user/apps_t2')
print(output)

# RICHIESTA INFORMAZIONI APPLICAZIONE CHE L'UTENTE è AUTORIZZATO AD ACCEDERE
print('\r\n## RICHIESTA INFORMAZIONI APPLICAZIONE CHE L\'UTENTE è AUTORIZZATO AD ACCEDERE')
output = API.SendRequest('app_t2/info',{'name':'articoli'})
print(output)

# RICHIESTA INFORMAZIONI APPLICAZIONE CHE L'UTENTE NON è AUTORIZZATO AD ACCEDERE
print('\r\n## RICHIESTA INFORMAZIONI APPLICAZIONE CHE L\'UTENTE NON è AUTORIZZATO AD ACCEDERE')
output = API.SendRequest('app_t2/info',{'name':'malattia'})
print(output)

#print('\r\n## IMPOSTO USER SESSION TOKEN ERRATO')
#API.UserSessionToken = '39f119842ebe582f049160f44bcd99f4'

# RICHIESTA INFORMAZIONI UTENTE
print('\r\n## RICHIESTA INFORMAZIONI UTENTE')
output = API.SendRequest('user/info')
print(output)

# RICHIESTA ELENCO AZIENDE UTENTE
print('\r\n## RICHIESTA ELENCO AZIENDE UTENTE')
output = API.SendRequest('user/companies')
print(output)

#LOGOUT UTENTE

print('\r\n## LOGOUT UTENTE')
output = API.SendRequest('user/logout')
print(output)

# RICHIESTA ELENCO AZIENDE UTENTE NON AUTENTICATO
print('\r\n## RICHIESTA ELENCO AZIENDE UTENTE NON AUTENTICATO')
output = API.SendRequest('user/companies')
print(output)


print('\r\n## TERMINO LA RICHIESTA INVIANDO IL COMANDO "api/logout" PER RICEVERE L\'API TOKEN DA APIX')
output = API.SendRequest('api/logout')
print(output)


# SECONDA CHIAMATA
print('\r\n## INVIO IL SECONDO COMANDO DI LOGIN API "api/login"')
output = API.SendRequest('api/login')
print(output)
API.ApiSessionToken = output.get('api-session-token')
print('\r\n## SESSION-TOKEN: '+API.ApiSessionToken)

print('\r\n## INVIO IL COMANDO "info/server"')
output = API.SendRequest('info/server')
print(output)

print('\r\n## TERMINO LA RICHIESTA INVIANDO IL COMANDO "api/logout" PER RICEVERE L\'API TOKEN DA APIX')
output = API.SendRequest('api/logout')
print(output)


#COMANDO INVIATO DOPO IL LOGOUT
print('\r\n## INIZIALIZZO LE API INVIANDO IL COMANDO "echo" CHE MI RESTITUIRà I PARAMETRI INVIATI TRAMITE POST, QUESTA VOLTA SENZA TOKEN')
output = API.SendRequest('debug/echo',{'test1':'prova1 senza token'})
print(output)

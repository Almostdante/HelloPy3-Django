from xmlrpc import client

xmlrpc_subtitles_url = 'https://api.opensubtitles.org:443/xml-rpc'

serverproxy = client.Server(xmlrpc_subtitles_url)
token = serverproxy.LogIn('', '', 'en', 'OSTestUserAgent')['token']
print (token)

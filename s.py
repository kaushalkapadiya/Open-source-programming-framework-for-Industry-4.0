

import request
import json


url='http://localhost:8080/api/1/things/org.eclipse.ditto:fancy-car/features/transmission/properties'
password='ditto'
data={
    'cur_speed' = 20
}

headers = {'Content-Type' : 'application/json'}

response=request.put(url,data=json.dumps(data),headers=headers,auth=('ditto','ditto'))

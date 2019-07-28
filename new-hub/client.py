#!/usr/bin/env python3

import requests as req

data = {'name': 'Peter'}

resp = req.post("http://localhost:8000/screenshot", data)
print(resp.text)
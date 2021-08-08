import requests
import json
from CONF import auth



class MessageTemplate():
	def __init__(self, adminID):
		token = auth.BOT_TOKEN
		self.senderID = adminID
		self.url = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(token)


	def genericTemplate(self, title=None, subtitle=None, image_url=None, buttons=[]):
		button_list = [{
				"type": "postback",
				"title": btn['title'],
				"payload": btn.get('action', 'DEVELOPER_DEFINED_PAYLOAD')
			} for btn in buttons]

		temp = {
			"recipient":{"id": self.senderID},
			"message":{
				"attachment":{
					"type":"template",
					"payload":{
						"template_type":"generic",
						"elements":[
						   {
							"title": title,
							"image_url": image_url,
							"subtitle": subtitle,
							"default_action": {
								"type": "web_url",
								"url": image_url,
								"webview_height_ratio": "tall",
							},
							"buttons": button_list    
							}
						]
					}
				}
			}
		}
		resp = requests.post(self.url, json=temp)
		return resp.json()


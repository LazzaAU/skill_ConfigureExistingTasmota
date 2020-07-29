from core.base.model.ProjectAliceObject import ProjectAliceObject


class CETConfigs(ProjectAliceObject):

	def __init__(self, deviceType: str, uid: str):
		super().__init__()
		self._brand = ''
		self._deviceType = deviceType
		self._uid = uid
		self._rule2 = ''
		self._location = ''
		self.backlogRules = ''
		self._sensorValue = ''
		self._switchMode = int
		self._switchTopic = int
		self._telePeriod = int

	@property
	def deviceType(self) -> str:
		return self._deviceType


	@property
	def uid(self) -> str:
		return self._uid

	@staticmethod
	def printResult(configs):
		print(f'Paste this following line into your Tasmota device\'s console ==>')
		print('')
		print(f'{configs}')

	##### Set the rules  ###
	def backlogConfigs(self):
		self.backlogRules = f'backlog MqttHost {self.Commons.getLocalIp()}; MqttClient {self._deviceType} - {self._location}; TelePeriod {self._telePeriod}; friendlyname {self._deviceType} - {self._location}; switchmode {self._switchMode}; switchtopic {self._switchTopic}; topic {self._uid}; grouptopic all; fulltopic projectalice/devices/tasmota/%prefix%/%topic%/; prefix1 cmd; prefix2 feedback; prefix3 feedback; rule1 on System#Boot do publish projectalice/devices/tasmota/feedback/hello/{self._uid} {{"siteId":"{self._location}","deviceType":"{self._deviceType}","uid":"{self._uid}"}} endon; rule1 1; {self._rule2}'
		self.printResult(configs=self.backlogRules)


	def getCETBacklogConfigs(self, location: str, brand: str) :
		if not brand:
			self._brand = 'generic'
		else:
			self._brand = brand

		self._location = location.name #ignore error, it works

		if 'BME280' in self._brand:
			self._sensorValue = 'Pressure'
		else:
			self._sensorValue = 'DewPoint'

		if 'EspEnvSensor' in self._deviceType:
			if self.checkCETSensorBrand(): #if sensor is a listed temperature sensor then do this
				self._switchMode = 0
				self._switchTopic = 0
				self._telePeriod = 300
				self._rule2 = f'rule2 on tele-{self._brand}#temperature do var1 %value% endon on tele-{self._brand}#Humidity do var2 %value% endon on tele-{self._brand}#{self._sensorValue} do var3 %value% endon on tele-{self._brand}#Temperature do event sendtemp endon on event#sendtemp do publish projectalice/devices/tasmota/feedback/{self._uid}/sensor {{"sensorBrand":"{self._brand}","sensorType":"temperatureSensor","siteId":"{self._location}","deviceType":"{self._deviceType}","Temperature":"%Var1%","Humidity":"%Var2%","{self._sensorValue}":"%Var3%","uid":"{self._uid}"}} endon; rule2 1; restart 1 '
				self.backlogConfigs()


		elif 'EspSwitch' in self._deviceType:  # if envSensor is not a listed temp sensor, like a pir or Lightsensor then do this
			self._switchMode = 2
			self._switchTopic = 0
			self._telePeriod = 0
			self._rule2 = f'rule2 on switch1#state do publish projectalice/devices/tasmota/feedback/{self._uid} {{"siteId":"{self._location}","deviceType":"{self._deviceType}","feedback":%value%,"uid":"{self._uid}"}} endon; rule2 1; restart 1'
			self.backlogConfigs()

		elif 'EspLightSensor' in self._deviceType:
			self._switchMode = 0
			self._switchTopic = 0
			self._telePeriod = 300
			self._rule2 = f'rule2 on tele-ANALOG#Illuminance do var1 %value% endon on tele-ANALOG#Illuminance do event sendAlicePayload endon on event#sendAlicePayload do publish projectalice/devices/tasmota/feedback/{self._uid}/sensor {{"sensorType":"ANALOG","siteId":"{self._location}","deviceType":"{self._deviceType}","Illuminance":"%Var1%","uid":"{self._uid}"}} endon; rule2 1; restart 1'
			self.backlogConfigs()


	def checkCETSensorBrand(self) -> bool:
		supportedSensors = ('BME680', 'BME280', 'DHT11', 'DHT22', 'AM2302', 'AM2301')
		if self._brand in supportedSensors:
			return True

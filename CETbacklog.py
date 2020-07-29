from core.base.model.ProjectAliceObject import ProjectAliceObject


class CETConfigs(ProjectAliceObject):

	def __init__(self, deviceType: str, uid: str):
		super().__init__()
		self._brand = ''
		self._deviceType = deviceType
		self._uid = uid
		self._rule2 = ''
		self._location = ''
		self.backlogSwitchConfigs = ''
		self._sensorValue = ''
		self._rule2Temp = ''
		self._rule2Switch = ''
		self._rule2LDR = ''

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

	##### Set the rule2 options  ###
	def backlogSwitchconfig(self):
		self.backlogSwitchConfigs = f'backlog MqttHost {self.Commons.getLocalIp()}; MqttClient {self._deviceType} - {self._location}; TelePeriod 0; friendlyname {self._deviceType} - {self._location}; switchmode 2; switchtopic 0; topic {self._uid}; grouptopic all; fulltopic projectalice/devices/tasmota/%prefix%/%topic%/; prefix1 cmd; prefix2 feedback; prefix3 feedback; rule1 on System#Boot do publish projectalice/devices/tasmota/feedback/hello/{self._uid} {{"siteId":"{self._location}","deviceType":"{self._deviceType}","uid":"{self._uid}"}} endon; rule1 1; {self._rule2Switch}'
		self.printResult(configs=self.backlogSwitchConfigs)

	def backlogTempconfig(self):
		backlogTempConfigs = f'backlog MqttHost {self.Commons.getLocalIp()}; MqttClient {self._deviceType} - {self._location}; TelePeriod 300; friendlyname {self._deviceType} - {self._location}; switchmode 0; switchtopic 0; topic {self._uid}; grouptopic all; fulltopic projectalice/devices/tasmota/%prefix%/%topic%/; prefix1 cmd; prefix2 feedback; prefix3 feedback; rule1 on System#Boot do publish projectalice/devices/tasmota/feedback/hello/{self._uid} {{"siteId":"{self._location}","deviceType":"{self._deviceType}","uid":"{self._uid}"}} endon; rule1 1; {self._rule2Temp}'
		self.printResult(configs=backlogTempConfigs)

	def backlogLDRconfig(self):
		backlogLDRConfigs = f'backlog MqttHost {self.Commons.getLocalIp()}; MqttClient {self._deviceType} - {self._location}; TelePeriod 300; friendlyname {self._deviceType} - {self._location}; switchmode 0; switchtopic 0; topic {self._uid}; grouptopic all; fulltopic projectalice/devices/tasmota/%prefix%/%topic%/; prefix1 cmd; prefix2 feedback; prefix3 feedback; rule1 on System#Boot do publish projectalice/devices/tasmota/feedback/hello/{self._uid} {{"siteId":"{self._location}","deviceType":"{self._deviceType}","uid":"{self._uid}"}} endon; rule1 1; {self._rule2LDR}'
		self.printResult(configs=backlogLDRConfigs)


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
				self._rule2Temp = f'rule2 on tele-{self._brand}#temperature do var1 %value% endon on tele-{self._brand}#Humidity do var2 %value% endon on tele-{self._brand}#{self._sensorValue} do var3 %value% endon on tele-{self._brand}#Temperature do event sendtemp endon on event#sendtemp do publish projectalice/devices/tasmota/feedback/{self._uid}/sensor {{"sensorBrand":"{self._brand}","sensorType":"temperatureSensor","siteId":"{self._location}","deviceType":"{self._deviceType}","Temperature":"%Var1%","Humidity":"%Var2%","{self._sensorValue}":"%Var3%","uid":"{self._uid}"}} endon '
				self.backlogTempconfig()

		elif 'EspSwitch' in self._deviceType:  # if envSensor is not a listed temp sensor, like a pir or Lightsensor then do this
			self._rule2Switch = f'rule2 on switch1#state do publish projectalice/devices/tasmota/feedback/{self._uid} {{"siteId":"{self._location}","deviceType":"{self._deviceType}","feedback":%value%,"uid":"{self._uid}"}} endon'
			self.backlogSwitchconfig()

		elif 'EspLightSensor' in self._deviceType:
			self._rule2LDR = f'rule2 on tele-ANALOG#Illuminance do var1 %value% endon on tele-ANALOG#Illuminance do event sendAlicePayload endon on event#sendAlicePayload do publish projectalice/devices/tasmota/feedback/{self._uid}/sensor {{"sensorType":"ANALOG","siteId":"{self._location}","deviceType":"{self._deviceType}","Illuminance":"%Var1%","uid":"{self._uid}"}} endon : rule2 1'
			self.backlogLDRconfig()

	def checkCETSensorBrand(self) -> bool:
		supportedSensors = ('BME680', 'BME280', 'DHT11', 'DHT22', 'AM2302', 'AM2301')
		if self._brand in supportedSensors:
			return True

from core.base.model.ProjectAliceObject import ProjectAliceObject
import inspect
from pathlib import Path

BACKLOGFILE = '/backLog.txt'


class CETConfigs(ProjectAliceObject):


	def __init__(self, deviceType: str, uid: str):
		super().__init__()
		self._deviceType = deviceType
		self._uid = uid
		self._location = ''
		self.backlogRules = ''
		self._switchMode = int
		self._switchTopic = int
		self._telePeriod = int
		self._skillPath = Path(inspect.getfile(self.__class__)).parent


	@property
	def deviceType(self) -> str:
		return self._deviceType


	@property
	def uid(self) -> str:
		return self._uid


	# def printResult(self,configs, backlogpath):

	##### Set the rules  ###
	def backlogConfigs(self):
		self.backlogRules = f'backlog MqttHost {self.Commons.getLocalIp()}; MqttClient {self._deviceType} - {self._location}; TelePeriod {self._telePeriod}; friendlyname {self._deviceType} - {self._location}; switchmode {self._switchMode}; switchtopic {self._switchTopic}; topic {self._uid}; grouptopic all; fulltopic projectalice/devices/tasmota/%prefix%/%topic%/; prefix1 cmd; prefix2 feedback; prefix3 feedback; rule1 on System#Boot do publish projectalice/devices/tasmota/feedback/hello/{self._uid} {{"siteId":"{self._location}","deviceType":"{self._deviceType}","uid":"{self._uid}"}} endon; rule1 1; restart 1'

		with open(f'{self._skillPath}{BACKLOGFILE}', 'w+') as file:
			file.write(self.backlogRules)

		self.logInfo(f'Open backlog.txt file from {self._skillPath}{BACKLOGFILE}')
		self.logInfo(f'nano {self._skillPath}{BACKLOGFILE}')
		self.logInfo(f'Then Paste that entire backlog command into your existing Tasmota Device console')


	def getCETBacklogConfigs(self, location: str, telePeriod):

		self._location = location.name  #NOSONAR ignore error, it works

		if 'EspEnvSensor' in self._deviceType or 'EspLightSensor' in self._deviceType:
			self._switchMode = 0
			self._switchTopic = 0
			self._telePeriod = telePeriod

			self.backlogConfigs()


		elif 'EspSwitch' in self._deviceType:  # if envSensor is not a listed temp sensor, like a pir or Lightsensor then do this
			self._switchMode = 2
			self._switchTopic = 0
			self._telePeriod = telePeriod
			self.backlogConfigs()

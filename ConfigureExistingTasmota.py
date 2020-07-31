from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler

from .CETbacklog import CETConfigs


class ConfigureExistingTasmota(AliceSkill):
	"""
	Author: LazzaAU
	Description: Configure a existing tasmota device to be alice compatible
	"""


	def __init__(self):
		super().__init__()
		self._uid = ''
		self._location: str = ''
		self._telePeriod: str = self.getConfig('telePeriod')
		self._deviceType = ''
		self._deviceClass: str = ''
		self._theSiteID = self.getAliceConfig('deviceName')
		self._counter = 0


	@IntentHandler('ConfigureTazDevice')
	def configureMyTasmota(self, session: DialogSession, **_kwargs):
		self._location = self.getConfig("locationOfDevice")

		if not self._location:
			self.endDialog(
				sessionId=session.sessionId,
				text='Please set a location first in the skill settings',
				siteId=session.siteId
			)
			return

		isitatemp: bool = self.getConfig("isItAtemperatureSensor")
		isitaswitch: bool = self.getConfig("isItASwitch")
		isitalightsensor: bool = self.getConfig("isItALightSensor")
		tempList = [isitatemp, isitaswitch, isitalightsensor]

		self._counter = 0
		for result in tempList:
			if result:
				self._counter += 1

		if self._counter > 1:
			self.endDialog(
				sessionId=session.sessionId,
				text='Please choose only one device type then re ask me to configure it',
				siteId=session.siteId
			)
			return

		if self.getConfig('isItASwitch'):
			self._deviceClass = 'EspSwitch'
		if self.getConfig('isItAtemperatureSensor') :
			self._deviceClass = 'EspEnvSensor'

		if self.getConfig('isItALightSensor'):

			self._deviceClass = 'EspLightSensor'
		self.processBacklogInputs(session)


	def processBacklogInputs(self, session: DialogSession):

		self.say(
			siteId=session.siteId,
			text='Ok give me a moment while i set up a backlog command for you. I\'ll print it in your logs'
		)
		# Create a Random UID for the database
		self._uid = self.DeviceManager.getFreeUID()
		self._deviceType = self.DeviceManager.getDeviceTypeByName(name=self._deviceClass)
		self._location = self.LocationManager.getLocation(location=self._location)
		self.DeviceManager.addNewDevice(deviceTypeId=self._deviceType.id, locationId=self._location.id, uid=self._uid)

		cetConfigs = CETConfigs(deviceType=self._deviceClass, uid=self._uid)
		confs = cetConfigs.getCETBacklogConfigs(self._location, self._telePeriod)

		if confs:
			print(f'{confs}')

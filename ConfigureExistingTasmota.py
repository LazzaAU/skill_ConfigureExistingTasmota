from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class ConfigureExistingTasmota(AliceSkill):
	"""
	Author: LazzaAU
	Description: Configure a existing tasmota device to be alice compatible
	"""

	@IntentHandler('MyIntentName')
	def dummyIntent(self, session: DialogSession, **_kwargs):
		pass

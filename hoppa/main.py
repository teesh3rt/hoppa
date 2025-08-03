from net import NetHandler
import log
from globals import VERSION, VERSION_CODENAME

log.info(f"hoppa v{VERSION} ({VERSION_CODENAME})", context="startup")
log.info("starting nethandler...", context="startup")
nh = NetHandler("0.0.0.0")
nh.listen()

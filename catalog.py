"""Knowledge base that gives telecom error codes their *meaning* (the 'semantic' layer)."""

# severity: Critical > Major > Minor > Info
SIP = {
    400: ("Bad Request", "Minor", "Signaling", "Malformed SIP message or header.", "Capture the INVITE and check header syntax / SBC normalisation rules."),
    401: ("Unauthorized", "Minor", "Authentication", "Credentials missing or rejected by registrar.", "Check digest credentials and realm; look for registration loops."),
    403: ("Forbidden", "Major", "Authentication", "Request understood but refused (barring, ACL, wrong trunk).", "Verify trunk ACLs, subscriber barring and roaming agreements."),
    404: ("Not Found", "Major", "Routing", "Called number / URI not found in routing or subscriber data.", "Check number analysis, ENUM/DNS and HSS/ENUM provisioning."),
    407: ("Proxy Authentication Required", "Minor", "Authentication", "Proxy demands authentication.", "Confirm UE/trunk answers the 407 challenge correctly."),
    408: ("Request Timeout", "Major", "Timeout", "No response from the next hop in time.", "Check connectivity, firewalls and overloaded next-hop nodes."),
    480: ("Temporarily Unavailable", "Minor", "Subscriber", "Callee currently not reachable (offline / not registered).", "Usually subscriber-side; confirm registration state."),
    481: ("Call/Transaction Does Not Exist", "Major", "Signaling", "Dialog state mismatch between nodes.", "Look for lost state after failover or asymmetric routing."),
    484: ("Address Incomplete", "Minor", "Routing", "Dialled number incomplete.", "Check digit collection / dial-plan on the originating side."),
    486: ("Busy Here", "Info", "Subscriber", "Callee busy.", "Normal behaviour; no network action."),
    487: ("Request Terminated", "Info", "Subscriber", "Caller cancelled before answer.", "Normal behaviour (CANCEL)."),
    488: ("Not Acceptable Here", "Major", "Media/Codec", "SDP offer rejected - codec or media mismatch.", "Compare offered codecs vs. peer capabilities; check transcoding on the SBC."),
    491: ("Request Pending", "Minor", "Signaling", "Glare - crossing re-INVITEs.", "Usually self-heals; check re-INVITE timers if frequent."),
    500: ("Server Internal Error", "Critical", "Server", "Unexpected condition on a SIP server.", "Inspect application server / CSCF logs for crashes."),
    502: ("Bad Gateway", "Critical", "Server", "Gateway got invalid response from upstream.", "Check the upstream node and interconnect link."),
    503: ("Service Unavailable", "Critical", "Overload", "Server overloaded or in maintenance.", "Check CPU/session limits, overload control and failover."),
    504: ("Server Time-out", "Critical", "Timeout", "Gateway timed out waiting on upstream.", "Check upstream latency and DNS resolution."),
    603: ("Decline", "Info", "Subscriber", "Callee explicitly declined.", "Normal behaviour."),
    604: ("Does Not Exist Anywhere", "Major", "Routing", "Number does not exist in any network.", "Verify number ranges and portability databases."),
}

# GTPv2-C cause values (3GPP TS 29.274). 16-19 are "accepted" and ignored as non-errors.
GTP = {
    64: ("Context not found", "Major", "Session", "Referenced bearer/PDN context does not exist.", "Check for timer expiry, restarts or out-of-sync state between SGW/PGW/MME."),
    65: ("Invalid message format", "Minor", "Signaling", "Malformed GTP message.", "Check vendor interop / GTP version support."),
    66: ("Version not supported", "Minor", "Signaling", "Peer does not support GTP version.", "Review GTP version negotiation."),
    67: ("Invalid length", "Minor", "Signaling", "Wrong message or IE length.", "Capture with Wireshark and compare IE lengths."),
    68: ("Service not supported", "Major", "Signaling", "Requested service not supported by peer.", "Check node feature licences/capabilities."),
    69: ("Mandatory IE incorrect", "Minor", "Signaling", "A mandatory IE has wrong value.", "Inspect IE contents in the offending message."),
    70: ("Mandatory IE missing", "Minor", "Signaling", "A mandatory IE is absent.", "Check sender implementation / interop."),
    72: ("System failure", "Critical", "Server", "Peer internal failure.", "Inspect SGW/PGW health and logs."),
    73: ("No resources available", "Critical", "Overload", "Peer out of resources (sessions/bearers).", "Check capacity, licence limits and session counters."),
    78: ("Missing or unknown APN", "Major", "Provisioning", "APN not configured on the gateway.", "Verify APN config and HSS subscription profile."),
    83: ("Preferred PDN type not supported", "Major", "Provisioning", "Requested IP type (v4/v6/v4v6) not supported.", "Align APN IP-type config and UE request."),
    84: ("All dynamic addresses occupied", "Critical", "Overload", "IP pool exhausted.", "Extend UE IP pools or reclaim stale sessions."),
    89: ("Denied in RAT", "Major", "Mobility", "Service denied in current radio access technology.", "Check RAT restrictions in subscription/policy."),
    94: ("Request rejected", "Major", "Session", "Request rejected, reason not specified.", "Look at the paired node's logs for the real reason."),
}

# Base Diameter result codes (RFC 6733). Only 3xxx/4xxx/5xxx are treated as errors.
DIAMETER = {
    3002: ("UNABLE_TO_DELIVER", "Critical", "Routing", "Message could not be delivered to destination.", "Check DRA/peer routing tables and peer state."),
    3004: ("TOO_BUSY", "Critical", "Overload", "Peer too busy to serve request.", "Check DRA/HSS/PCRF load and throttling."),
    3007: ("APPLICATION_UNSUPPORTED", "Major", "Signaling", "Application-Id not supported.", "Verify Diameter application support on the peer."),
    4001: ("AUTHENTICATION_REJECTED", "Major", "Authentication", "Authentication rejected.", "Check subscriber credentials / AuC data."),
    5001: ("AVP_UNSUPPORTED", "Minor", "Signaling", "Mandatory AVP not supported.", "Check dictionary/version alignment."),
    5003: ("AUTHORIZATION_REJECTED", "Major", "Authentication", "User not authorised for the service.", "Review subscription and policy profile."),
    5004: ("INVALID_AVP_VALUE", "Minor", "Signaling", "AVP carries invalid value.", "Inspect the offending AVP."),
    5005: ("MISSING_AVP", "Minor", "Signaling", "Required AVP missing.", "Compare message with the 3GPP interface spec."),
    5012: ("UNABLE_TO_COMPLY", "Major", "Server", "Request can't be fulfilled.", "Inspect the answering node's logs."),
}

ACCEPTED_GTP = {16, 17, 18, 19}
CATALOGS = {"SIP": SIP, "GTP": GTP, "Diameter": DIAMETER}
SEVERITY_ORDER = ["Critical", "Major", "Minor", "Info"]

import random, datetime as dt
random.seed(7)
t = dt.datetime(2026, 11, 6, 9, 0, 0)
ips = ["10.20.1.11", "10.20.1.12", "10.20.2.5", "172.16.8.4", "192.168.50.9"]
msgs = [
 (30, "{ts} {ip} scscf INFO SIP/2.0 200 OK Call-ID: a{n}@ims.example"),
 (12, "{ts} {ip} pcscf WARN SIP/2.0 404 Not Found Call-ID: a{n}@ims.example"),
 (9,  "{ts} {ip} sbc ERROR SIP/2.0 488 Not Acceptable Here (codec mismatch) Call-ID: a{n}@ims.example"),
 (5,  "{ts} {ip} scscf ERROR SIP 503 Service Unavailable overload"),
 (3,  "{ts} {ip} icscf WARN SIP/2.0 408 Request Timeout"),
 (2,  "{ts} {ip} pcscf WARN SIP/2.0 486 Busy Here"),
 (8,  "{ts} {ip} sgw WARN GTPv2 Create Session Response cause 78 (Missing or unknown APN)"),
 (5,  "{ts} {ip} pgw ERROR GTPv2 Create Session Response cause=73 No resources available"),
 (4,  "{ts} {ip} sgw WARN GTPv2 Modify Bearer cause 64 context not found"),
 (3,  "{ts} {ip} pgw ERROR GTPv2 cause: 84 All dynamic addresses occupied"),
 (10, "{ts} {ip} sgw INFO GTPv2 Create Session Response cause 16 Request accepted"),
 (3,  "{ts} {ip} dra ERROR Diameter S6a Result-Code: 3002 UNABLE_TO_DELIVER"),
 (2,  "{ts} {ip} pcrf WARN Diameter Gx Result-Code = 5012"),
 (4,  "{ts} {ip} amf DEBUG heartbeat ok"),
]
pool = [m for w, m in msgs for _ in range(w)]
with open("sample_logs/This_Is_A_Sample.log", "w") as f:
    for n in range(600):
        t += dt.timedelta(seconds=random.randint(1, 6))
        f.write(random.choice(pool).format(ts=t.strftime("%Y-%m-%d %H:%M:%S"), ip=random.choice(ips), n=n) + "\n")

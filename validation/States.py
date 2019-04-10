import enum


class States(enum.Enum):
    FAIL = -1
    START = 0
    BASE = 1
    SUCCESS = 2

    # DNS Record Types
    A = "A"
    A4 = "AAAA"
    CNAME = "CNAME"
    DNAME = "DNAME"
    HIP = "HIP"
    KX = "KX"
    LOC = "LOC"
    MX = "MX"
    NAPTR = "NAPTR"
    NS = "NS"
    PTR = "PTR"
    SMIMEA = "SMIMEA"
    SOA = "SOA"
    SRV = "SRV"
    URI = "URI"

APP_TITLE       = "Honeypot Dashboard"

STARTING_DATE = "2026-05-27"
LAST_DATE    = "2026-06-03"

TIME_RANGE = {
    1: "Last day",
    3: "Last 3 days",
    8: "Full period (May 27 – Jun 3)",
}

HONEYPOTS = [
    "All",
    "p0f",           
    "suricata",      
    "honeytrap",     
    "fatt",          
    "nginx",         
    "dionaea",       
    "cowrie",       
    "miniprint",     
    "tanner",        
    "h0neytr4p",     
    "adbhoney",      
    "ciscoasa",     
    "conpot",        
    "mailoney",      
    "redishoneypot", 
    "honeyaml",      
    "elasticpot",    
    "heralding",     
]

PORT_NAMES = {
    21:    "FTP",
    22:    "SSH",
    23:    "Telnet",
    25:    "SMTP",
    80:    "HTTP",
    443:   "HTTPS",
    445:   "SMB",
    1433:  "MSSQL",
    3306:  "MySQL",
    3389:  "RDP",
    5432:  "PostgreSQL",
    6379:  "Redis",
    8080:  "HTTP-alt",
    8443:  "HTTPS-alt",
    27017: "MongoDB",
}

SEVERITY_MAP = {
    1: "Critical",
    2: "High",
    3: "Medium",
    4: "Low",
}

SEVERITY_COLORS = {
    "Critical":   "#e63946",
    "High":       "#f4a261",
    "Medium":     "#e9c46a",
    "Low":        "#2a9d8f",
    "Unknown":    "#adb5bd",
}

CACHE_TTL = 3600
TOP_N = 12

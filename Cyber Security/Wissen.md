# Browser-Tools
1.Elemente
2.Konsole
3.Netzwerk
4.(localer) Speicher

# API = Application Progamming Interface

curl *api_endpoint*
curl -H "x-api-key: ??" *api_endpoint*

# XSS-Angriff
script>alert("Hi")alert("Hi") script/>
img src=y onerror="Hi">

# LLM Promt Injection
curl *api_endpoint*

# SQL = Structured Query Language 
Select * FROM students WHERE name = '%' OR 1=1-- 

1.' OR 1=1
2.' UNION SELECT * FROM sqlite_master --
3.' UNION SELECT 1,2,3,4 FROM sqlite_master --
4.' UNION SELECT '1','2','3','4' FROM sqlite_master --

# JWT = JSON Web Tokens
Token sind im lokalen speicher
Aufbau: header.payload/inhalt.signatur

**42 antwort auf alles**

# SSTI
debug_info 
internal_data
config
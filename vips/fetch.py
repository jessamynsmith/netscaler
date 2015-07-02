import re
from pexpect import spawn, TIMEOUT

SSH_NEWKEY = 'Are you sure you want to continue connecting'

class Netscaler(object):
    """
    wrapper class for interacting with expect and the netscaler
    """
    def __init__(self,
                 host='',
                 username='',
                 password=''
                 ):
        """
        :param host: string
        :param username: string
        :param password: string
        """
        self.host = host
        self.username = username
        self.password = password
        self.prompt = '>'

    def _send(self, command=''):

        self._session()
        self.session.sendline(command)
        self.session.expect(self.prompt)
        result = self.session.before
        self.session.sendline('exit')
        return result

    def _session(self):
        """
        attempt to create an expect session, if there is timeout return false
        :return: true or false
        """
        session = spawn('ssh %s@%s' % (self.username, self.host))
        session.delaybeforesend = 1
        session.timeout = 4
        retval = session.expect([SSH_NEWKEY, 'password:'])

        if retval == 0:
            session.sendline('yes')
            session.expect('password:')

        session.sendline(self.password)

        session.expect(self.prompt)
        self.session = session
        return True

    def get_servers(self):
        """
        returns the output form 'show server' this is a list of servers
        :return:
        """

        data = self._send('show server')
        # parse out the data so we get a format that can be chanted into a dict
        data = re.sub(r'\r\n\d+\)|\r\n', '', data)
        data = re.sub(r':\s+', ':', data)
        data = re.split(r'\s+', data)[3:]
        result = {}
        id = 0

        for i in xrange(0, len(data), 3):
            temp = {}

            for j in range(0, 3):
                if data[i+j] == 'Done':
                    break

                temp2 = re.split(r':', data[i+j])
                temp.update({temp2[0]: temp2[1]})

            if temp != {}:
                result[id] = temp
                id += 1

        return result

    def get_vips(self):
        """
        returns the output from 'show lb vserver' as a dict
        :return:
        """
        keys = ['label', 'address', 'port', 'state', 'effective state']
        data = self._send('show lb vserver')
        data = re.split(r'\r\n\d+\)', data)[1:]
        result = {}

        for id, vip in enumerate(data):
            matchObj = re.match(r'^\t(\S+)\s\((\d+.\d+.\d+.\d+):(\d+)\)\s-\s\w+\t\w+:\s\w+\s\r\n\tState:\s(\w+)\r\n\tEffective\sState:\s(\w+)', vip)

            if matchObj:
                temp = {}
                for indx, val in enumerate(keys):
                    # have to add +1 because re groups start at 1 0 would be the whole match
                    #print val, matchObj.group(indx+1)
                    temp.update({val: matchObj.group(indx+1)})

                result[id] = temp

        return result

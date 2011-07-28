'''
Publish a command from a minion to a target
'''
# Import salt libs
import salt.crypt
# Import ZeroMQ
import zmq

def _get_socket():
    '''
    Return the ZeroMQ socket to use
    '''
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(__opts__['master_uri'])
    return socket


def publish(tgt, fun, arg, expr_form='glob', returner=''):
    '''
    Publish a command from the minion out to other minions, publications need
    to be enabled on the Salt master and the minion needs to have permission
    to publish the command. The Salt master will also prevent a recursive
    publication loop, this means that a minion cannot command another minion
    to command another minion as that would create an infinate command loop.

    CLI Example:
    salt '*' publish.publish
    '''
    if fun == 'publish.publish':
        # Need to log something here
        return {}
    auth = salt.crypt.SAuth(__opts__)
    tok = auth.gen_token('salt')
    payload = {'enc': 'aes'}
    load = {
            'fun': fun,
            'arg': arg,
            'tgt': tgt,
            'ret': returner,
            'tok': tok,
            'id': __opts__['id']}
    payload['load'] = self.auth.crypticle.dumps(load)
    socket = __get_socket()
    socket.send_pyobj(payload)
    return auth.crypticle.loads(self.socket.recv_pyobj())

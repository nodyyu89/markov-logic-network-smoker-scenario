import signal as signal_
import threading
from collections import defaultdict

__usrreg = defaultdict(list)
__sysinit = defaultdict(list)
__systerm = defaultdict(list)

SIGINT = signal_.SIGINT
SIGTERM = signal_.SIGTERM
#SIGKILL = signal_.SIGKILL
SIGABRT = signal_.SIGABRT
#SIGALRM = signal_.SIGALRM
#SIGBUS = signal_.SIGBUS
#SIGCHLD = signal_.SIGCHLD
#SIGCLD = signal_.SIGCLD
#SIGCONT = signal_.SIGCONT
SIGFPE = signal_.SIGFPE
#SIGHUP = signal_.SIGHUP
SIGILL = signal_.SIGILL
SIGINT = signal_.SIGINT
#SIGIO = signal_.SIGIO
#SIGIOT = signal_.SIGIO
#SIGKILL = signal_.SIGKILL
#SIGPIPE = signal_.SIGPIPE
#SIGPOLL = signal_.SIGPOLL
#SIGPROF = signal_.SIGPROF
# =============================================================================
# SIGPWR = signal_.SIGPWR
# SIGQUIT = signal_.SIGQUIT
# SIGRTMAX = signal_.SIGRTMAX
# SIGRTMIN = signal_.SIGRTMIN
SIGSEGV = signal_.SIGSEGV
# SIGSTOP = signal_.SIGSTOP
# SIGSYS = signal_.SIGSYS
SIGTERM = signal_.SIGTERM
# SIGTRAP = signal_.SIGTRAP
# SIGTSTP = signal_.SIGTSTP
# SIGTTIN = signal_.SIGTTIN
# SIGTTOU = signal_.SIGTTOU
# SIGURG = signal_.SIGURG
# SIGUSR1 = signal_.SIGUSR1
# SIGUSR2 = signal_.SIGUSR2
# SIGVTALRM = signal_.SIGVTALRM
# SIGWINCH = signal_.SIGWINCH
# SIGXCPU = signal_.SIGXCPU
# SIGXFSZ = signal_.SIGXFSZ
# =============================================================================

_lock = threading.Lock()


def _run_handlers(signal, args):
    '''Executes all handlers that are registered for the given
    siganl in the order of registration.'''
    # run system handlers for preparing the signal handling
    for handler in __sysinit[signal]:
        handler(*args)
    # run user defined signal handlers
    for handler in __usrreg[signal]:
        handler(*args)
    # run system handlers for cleaning up the signal handling
    for handler in __systerm[signal]:
        handler(*args)


def add_handler(signal, handler):
    '''
    Add a handler to be executed on the signal ``signal``

    :param signal:  the signal to react to.
    :param handler: a callable that will be called on the signal.
    :return:
    '''
    _add_handler(signal, handler, __usrreg)


def _add_handler(signal, handler, registry):
    '''
    Add a handler to be executed on the signal ``signal``

    :param signal:  the signal to react to.
    :param handler: a callable that will be called on the signal.
    :return:
    '''
    with _lock:
        handlers_ = registry[signal]
        if not handlers_:
            signal_.signal(signal, lambda *args: _run_handlers(signal, args))
        if handler not in handlers_:
            handlers_.insert(0, handler)


def rm_handler(signal, handler):
    '''
    Remove a handler if it is registered to the given signal.
    :param signal:  the signal that the handler is registered for
    :param handler: the handler function.
    :return:
    '''
    _rm_handler(signal, handler, __usrreg)


def _rm_handler(signal, handler, registry):
    '''
    Remove a handler if it is registered to the given signal.
    :param signal:  the signal that the handler is registered for
    :param handler: the handler function.
    :return:
    '''
    with _lock:
        try:
            registry[signal].remove(handler)
        except ValueError:
            pass


def keyint(*_):
    raise KeyboardInterrupt()


def enable_ctrlc():
    '''
    Allows to interrupt the main thread by pressing Ctrl-C.
    :return:
    '''
    _add_handler(SIGINT, keyint, __systerm)


def disable_ctrlc():
    '''
    Disables interruption of the main thread by the Ctrl-C key combination.
    :return:
    '''
    _rm_handler(SIGINT, keyint, __systerm)

# -*- coding: utf-8 -*-
'''
The sys module provides information about the available functions on the minion
'''
from __future__ import absolute_import

# Import python libs
import fnmatch
import logging

# Import salt libs
import salt.loader
import salt.utils
import salt.state
import salt.runner
from salt.utils.doc import strip_rst as _strip_rst

# Import 3rd-party libs
import salt.ext.six as six

log = logging.getLogger(__name__)

# Define the module's virtual name
__virtualname__ = 'sys'

__proxyenabled__ = ['*']


def __virtual__():
    '''
    Return as sys
    '''
    return __virtualname__


def doc(*args):
    '''
    Return the docstrings for all modules. Optionally, specify a module or a
    function to narrow the selection.

    The strings are aggregated into a single document on the master for easy
    reading.

    Multiple modules/functions can be specified.

    CLI Example:

    .. code-block:: bash

        salt '*' sys.doc
        salt '*' sys.doc sys
        salt '*' sys.doc sys.doc
        salt '*' sys.doc network.traceroute user.info

    Modules can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.doc 'sys.*'
        salt '*' sys.doc 'sys.list_*'
    '''
    docs = {}
    if not args:
        for fun in __salt__:
            docs[fun] = __salt__[fun].__doc__
        return _strip_rst(docs)

    for module in args:
        _use_fnmatch = False
        if '*' in module:
            target_mod = module
            _use_fnmatch = True
        elif module:
            # allow both "sys" and "sys." to match sys, without also matching
            # sysctl
            target_mod = module + '.' if not module.endswith('.') else module
        else:
            target_mod = ''
        if _use_fnmatch:
            for fun in fnmatch.filter(__salt__.keys(), target_mod):  # pylint: disable=incompatible-py3-code
                docs[fun] = __salt__[fun].__doc__                    # There's no problem feeding fnmatch.filter()
        else:                                                        # with a Py3's dict_keys() instance

            for fun in __salt__:
                if fun == module or fun.startswith(target_mod):
                    docs[fun] = __salt__[fun].__doc__
    return _strip_rst(docs)


def state_doc(*args):
    '''
    Return the docstrings for all states. Optionally, specify a state or a
    function to narrow the selection.

    The strings are aggregated into a single document on the master for easy
    reading.

    Multiple states/functions can be specified.

    .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.state_doc
        salt '*' sys.state_doc service
        salt '*' sys.state_doc service.running
        salt '*' sys.state_doc service.running ipables.append

    State names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.state_doc 'service.*' 'iptables.*'

    '''
    st_ = salt.state.State(__opts__)

    docs = {}
    if not args:
        for fun in st_.states:
            state = fun.split('.')[0]
            if state not in docs:
                if hasattr(st_.states[fun], '__globals__'):
                    docs[state] = st_.states[fun].__globals__['__doc__']
            docs[fun] = st_.states[fun].__doc__
        return _strip_rst(docs)

    for module in args:
        _use_fnmatch = False
        if '*' in module:
            target_mod = module
            _use_fnmatch = True
        elif module:
            # allow both "sys" and "sys." to match sys, without also matching
            # sysctl
            target_mod = module + '.' if not module.endswith('.') else module
        else:
            target_mod = ''
        if _use_fnmatch:
            for fun in fnmatch.filter(st_.states, target_mod):
                state = fun.split('.')[0]
                if hasattr(st_.states[fun], '__globals__'):
                    docs[state] = st_.states[fun].__globals__['__doc__']
                docs[fun] = st_.states[fun].__doc__
        else:
            for fun in st_.states:
                if fun == module or fun.startswith(target_mod):
                    state = module.split('.')[0]
                    if state not in docs:
                        if hasattr(st_.states[fun], '__globals__'):
                            docs[state] = st_.states[fun].__globals__['__doc__']
                    docs[fun] = st_.states[fun].__doc__
    return _strip_rst(docs)


def runner_doc(*args):
    '''
    Return the docstrings for all runners. Optionally, specify a runner or a
    function to narrow the selection.

    The strings are aggregated into a single document on the master for easy
    reading.

    Multiple runners/functions can be specified.

    .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.runner_doc
        salt '*' sys.runner_doc cache
        salt '*' sys.runner_doc cache.grains
        salt '*' sys.runner_doc cache.grains mine.get

    Runner names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.runner_doc 'cache.clear_*'

    '''
    run_ = salt.runner.Runner(__opts__)
    docs = {}
    if not args:
        for fun in run_.functions:
            docs[fun] = run_.functions[fun].__doc__
        return _strip_rst(docs)

    for module in args:
        _use_fnmatch = False
        if '*' in module:
            target_mod = module
            _use_fnmatch = True
        elif module:
            # allow both "sys" and "sys." to match sys, without also matching
            # sysctl
            target_mod = module + '.' if not module.endswith('.') else module
        else:
            target_mod = ''
        if _use_fnmatch:
            for fun in fnmatch.filter(run_.functions, target_mod):
                docs[fun] = run_.functions[fun].__doc__
        else:
            for fun in run_.functions:
                if fun == module or fun.startswith(target_mod):
                    docs[fun] = run_.functions[fun].__doc__
    return _strip_rst(docs)


def returner_doc(*args):
    '''
    Return the docstrings for all returners. Optionally, specify a returner or a
    function to narrow the selection.

    The strings are aggregated into a single document on the master for easy
    reading.

    Multiple returners/functions can be specified.

    .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.returner_doc
        salt '*' sys.returner_doc sqlite3
        salt '*' sys.returner_doc sqlite3.get_fun
        salt '*' sys.returner_doc sqlite3.get_fun etcd.get_fun

    Returner names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.returner_doc 'sqlite3.get_*'

    '''

    returners_ = salt.loader.returners(__opts__, [])
    docs = {}
    if not args:
        for fun in returners_:
            docs[fun] = returners_[fun].__doc__
        return _strip_rst(docs)

    for module in args:
        _use_fnmatch = False
        if '*' in module:
            target_mod = module
            _use_fnmatch = True
        elif module:
            # allow both "sys" and "sys." to match sys, without also matching
            # sysctl
            target_mod = module + '.' if not module.endswith('.') else module
        else:
            target_mod = ''
        if _use_fnmatch:
            for fun in returners_:
                if fun == module or fun.startswith(target_mod):
                    docs[fun] = returners_[fun].__doc__
        else:
            for fun in six.iterkeys(returners_):
                if fun == module or fun.startswith(target_mod):
                    docs[fun] = returners_[fun].__doc__
    return _strip_rst(docs)


def renderer_doc(*args):
    '''
    Return the docstrings for all renderers. Optionally, specify a renderer or a
    function to narrow the selection.

    The strings are aggregated into a single document on the master for easy
    reading.

    Multiple renderers can be specified.

    .. versionadded:: 2015.5.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.renderer_doc
        salt '*' sys.renderer_doc cheetah
        salt '*' sys.renderer_doc jinja json

    Renderer names can be specified as globs.

    .. code-block:: bash

        salt '*' sys.renderer_doc 'c*' 'j*'

    '''
    renderers_ = salt.loader.render(__opts__, [])
    docs = {}
    if not args:
        for fun in six.iterkeys(renderers_):
            docs[fun] = renderers_[fun].__doc__
        return _strip_rst(docs)

    for module in args:
        if '*' in module:
            for fun in fnmatch.filter(renderers_.keys(), module):   # pylint: disable=incompatible-py3-code
                docs[fun] = renderers_[fun].__doc__                 # There's no problem feeding fnmatch.filter()
                                                                    # with a Py3's dict_keys() instance
        else:
            for fun in six.iterkeys(renderers_):
                docs[fun] = renderers_[fun].__doc__
    return _strip_rst(docs)


def list_functions(*args, **kwargs):  # pylint: disable=unused-argument
    '''
    List the functions for all modules. Optionally, specify a module or modules
    from which to list.

    CLI Example:

    .. code-block:: bash

        salt '*' sys.list_functions
        salt '*' sys.list_functions sys
        salt '*' sys.list_functions sys user

    Function names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.list_functions 'sys.list_*'

    '''
    # ## NOTE: **kwargs is used here to prevent a traceback when garbage
    # ##       arguments are tacked on to the end.

    if not args:
        # We're being asked for all functions
        return sorted(__salt__)

    names = set()
    for module in args:
        _use_fnmatch = False
        if '*' in module:
            target_mod = module
            _use_fnmatch = True
        elif module:
            # allow both "sys" and "sys." to match sys, without also matching
            # sysctl
            module = module + '.' if not module.endswith('.') else module
        if _use_fnmatch:
            for func in fnmatch.filter(__salt__, target_mod):
                names.add(func)
        else:
            for func in __salt__:
                if func.startswith(module):
                    names.add(func)
    return sorted(names)


def list_modules(*args):
    '''
    List the modules loaded on the minion

    .. versionadded:: 2015.5.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.list_modules

    Module names can be specified as globs.

    .. code-block:: bash

        salt '*' sys.list_modules 's*'

    '''
    modules = set()
    if not args:
        for func in __salt__:
            comps = func.split('.')
            if len(comps) < 2:
                continue
            modules.add(comps[0])
        return sorted(modules)

    for module in args:
        for func in fnmatch.filter(__salt__, module):
            comps = func.split('.')
            if len(comps) < 2:
                continue
            modules.add(comps[0])
    return sorted(modules)


def reload_modules():
    '''
    Tell the minion to reload the execution modules

    CLI Example:

    .. code-block:: bash

        salt '*' sys.reload_modules
    '''
    # This is handled inside the minion.py file, the function is caught before
    # it ever gets here
    return True


def argspec(module=''):
    '''
    Return the argument specification of functions in Salt execution
    modules.

    CLI Example:

    .. code-block:: bash

        salt '*' sys.argspec pkg.install
        salt '*' sys.argspec sys
        salt '*' sys.argspec

    Module names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.argspec 'pkg.*'

    '''
    return salt.utils.argspec_report(__salt__, module)


def state_argspec(module=''):
    '''
    Return the argument specification of functions in Salt state
    modules.

    .. versionadded:: 2015.5.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.state_argspec pkg.installed
        salt '*' sys.state_argspec file
        salt '*' sys.state_argspec

    State names can be specified as globs.

    .. code-block:: bash

        salt '*' sys.state_argspec 'pkg.*'

    '''
    st_ = salt.state.State(__opts__)
    return salt.utils.argspec_report(st_.states, module)


def returner_argspec(module=''):
    '''
    Return the argument specification of functions in Salt returner
    modules.

    .. versionadded:: 2015.5.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.returner_argspec xmpp
        salt '*' sys.returner_argspec xmpp smtp
        salt '*' sys.returner_argspec

    Returner names can be specified as globs.

    .. code-block:: bash

        salt '*' sys.returner_argspec 'sqlite3.*'

    '''
    returners_ = salt.loader.returners(__opts__, [])
    return salt.utils.argspec_report(returners_, module)


def runner_argspec(module=''):
    '''
    Return the argument specification of functions in Salt runner
    modules.

    .. versionadded:: 2015.5.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.runner_argspec state
        salt '*' sys.runner_argspec http
        salt '*' sys.runner_argspec

    Runner names can be specified as globs.

    .. code-block:: bash

        salt '*' sys.runner_argspec 'winrepo.*'
    '''
    run_ = salt.runner.Runner(__opts__)
    return salt.utils.argspec_report(run_.functions, module)


def list_state_functions(*args, **kwargs):  # pylint: disable=unused-argument
    '''
    List the functions for all state modules. Optionally, specify a state
    module or modules from which to list.

    .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.list_state_functions
        salt '*' sys.list_state_functions file
        salt '*' sys.list_state_functions pkg user

    State function names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.list_state_functions 'file.*'
        salt '*' sys.list_state_functions 'file.s*'

    '''
    # NOTE: **kwargs is used here to prevent a traceback when garbage
    #       arguments are tacked on to the end.

    st_ = salt.state.State(__opts__)
    if not args:
        # We're being asked for all functions
        return sorted(st_.states)

    names = set()
    for module in args:
        _use_fnmatch = False
        if '*' in module:
            target_mod = module
            _use_fnmatch = True
        elif module:
            # allow both "sys" and "sys." to match sys, without also matching
            # sysctl
            module = module + '.' if not module.endswith('.') else module
        if _use_fnmatch:
            for func in fnmatch.filter(st_.states, target_mod):
                names.add(func)
        else:
            for func in st_.states:
                if func.startswith(module):
                    names.add(func)
    return sorted(names)


def list_state_modules(*args):
    '''
    List the modules loaded on the minion

    .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.list_state_modules

    State module names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.list_state_modules 'mysql_*'

    '''
    st_ = salt.state.State(__opts__)
    modules = set()

    if not args:
        for func in st_.states:
            log.debug('func {0}'.format(func))
            comps = func.split('.')
            if len(comps) < 2:
                continue
            modules.add(comps[0])
        return sorted(modules)

    for module in args:
        for func in fnmatch.filter(st_.states, module):
            comps = func.split('.')
            if len(comps) < 2:
                continue
            modules.add(comps[0])
    return sorted(modules)


def list_runners(*args):
    '''
    List the runners loaded on the minion

    .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.list_runners

    Runner names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.list_runners 'm*'

    '''
    run_ = salt.runner.Runner(__opts__)
    runners = set()
    if not args:
        for func in run_.functions:
            comps = func.split('.')
            if len(comps) < 2:
                continue
            runners.add(comps[0])
        return sorted(runners)

    for module in args:
        for func in fnmatch.filter(run_.functions, module):
            comps = func.split('.')
            if len(comps) < 2:
                continue
            runners.add(comps[0])
    return sorted(runners)


def list_runner_functions(*args, **kwargs):  # pylint: disable=unused-argument
    '''
    List the functions for all runner modules. Optionally, specify a runner
    module or modules from which to list.

    .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.list_runner_functions
        salt '*' sys.list_runner_functions state
        salt '*' sys.list_runner_functions state virt

    Runner function names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.list_runner_functions 'state.*' 'virt.*'

    '''
    # ## NOTE: **kwargs is used here to prevent a traceback when garbage
    # ##       arguments are tacked on to the end.

    run_ = salt.runner.Runner(__opts__)
    if not args:
        # We're being asked for all functions
        return sorted(run_.functions)

    names = set()
    for module in args:
        _use_fnmatch = False
        if '*' in module:
            target_mod = module
            _use_fnmatch = True
        elif module:
            # allow both "sys" and "sys." to match sys, without also matching
            # sysctl
            module = module + '.' if not module.endswith('.') else module
        if _use_fnmatch:
            for func in fnmatch.filter(run_.functions, target_mod):
                names.add(func)
        else:
            for func in run_.functions:
                if func.startswith(module):
                    names.add(func)
    return sorted(names)


def list_returners(*args):
    '''
    List the returners loaded on the minion

    .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.list_returners

    Returner names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.list_returners 's*'

    '''
    returners_ = salt.loader.returners(__opts__, [])
    returners = set()

    if not args:
        for func in six.iterkeys(returners_):
            comps = func.split('.')
            if len(comps) < 2:
                continue
            returners.add(comps[0])
        return sorted(returners)

    for module in args:
        for func in fnmatch.filter(returners_.keys(), module):  # pylint: disable=incompatible-py3-code
            comps = func.split('.')                             # There's no problem feeding fnmatch.filter()
            if len(comps) < 2:                                  # with a Py3's dict_keys() instance
                continue
            returners.add(comps[0])
    return sorted(returners)


def list_returner_functions(*args, **kwargs):  # pylint: disable=unused-argument
    '''
    List the functions for all returner modules. Optionally, specify a returner
    module or modules from which to list.

    .. versionadded:: 2014.7.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.list_returner_functions
        salt '*' sys.list_returner_functions mysql
        salt '*' sys.list_returner_functions mysql etcd

    Returner names can be specified as globs.

    .. versionadded:: 2015.5.0

    .. code-block:: bash

        salt '*' sys.list_returner_functions 'sqlite3.get_*'

    '''
    # NOTE: **kwargs is used here to prevent a traceback when garbage
    #       arguments are tacked on to the end.

    returners_ = salt.loader.returners(__opts__, [])
    if not args:
        # We're being asked for all functions
        return sorted(returners_)

    names = set()
    for module in args:
        _use_fnmatch = False
        if '*' in module:
            target_mod = module
            _use_fnmatch = True
        elif module:
            # allow both "sys" and "sys." to match sys, without also matching
            # sysctl
            module = module + '.' if not module.endswith('.') else module
        if _use_fnmatch:
            for func in returners_:
                if func.startswith(module):
                    names.add(func)
        else:
            for func in six.iterkeys(returners_):
                if func.startswith(module):
                    names.add(func)
    return sorted(names)


def list_renderers(*args):
    '''
    List the renderers loaded on the minion

    .. versionadded:: 2015.5.0

    CLI Example:

    .. code-block:: bash

        salt '*' sys.list_renderers

    Render names can be specified as globs.

    .. code-block:: bash

        salt '*' sys.list_renderers 'yaml*'

    '''
    ren_ = salt.loader.render(__opts__, [])
    ren = set()

    if not args:
        for func in six.iterkeys(ren_):
            ren.add(func)
        return sorted(ren)

    for module in args:
        for func in fnmatch.filter(ren_, module):
            ren.add(func)
    return sorted(ren)

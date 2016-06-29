import sys
import os

def update(project_name, command='update', modules='app.yaml', version=None, app_id=None):

    #os.system('cp yaml/%s/*.yaml .' % project_name)

    cmd = 'appcfg.py --oauth2 %s %s' % (command, modules)
    cmd = cmd + ' -V %s' % version if version is not None else cmd
    cmd = cmd + ' -A %s' % app_id if app_id is not None else cmd

    print '''
    *****
    RUNNING:  %s

    ''' % cmd

    os.system(cmd)
    #os.system('rm *.yaml')

def usage():
    return '''
        ------
        Usage:
        ------
        python update.py --project
              project name, as specified in "yaml" folder.
              -> updates the whole project (app.yaml + all modules)

        -----------------
        optional options:
        -----------------
        --modules:  comma-separated string
        --dispatch: update_dispatch
        --indexes:  update_indexes
        --queues:   update_queues
        --cron:     update_cron

        --rollback: rollback project
        --version:  specify a version
        --app_id:   specify an app_id

        ---------
        examples:
        ---------
        python update.py --project youtab
        python update.py --project prospero --modules billing.yaml,backoffice.yaml
        python update.py --project wixprivatemedia-gptest --queues
        python update.py --project castlebuilders rollback
        '''

def main(args):

    if '--help' in args:
        print usage()
        return

    app_id  = None
    version = None

    if '--project' in args:
        proj_index = args.index('--project')
        proj = (args[proj_index + 1])
    else:
        print '\n                * project name (--project) is missing! *\n' \
              '        To learn how to use the script, try python update.py --help\n'
        return

    if '--version' in args:
        version_index = args.index('--version')
        version = args[version_index + 1]

    if '--app_id' in args:
        app_id_index = args.index('--app_id')
        app_id = args[app_id_index + 1]

    if '--modules' in args:
        modules_index = args.index('--modules')
        modules = args[modules_index + 1].split(',')

        modules_str = ''
        for module in modules:
            modules_str += module + ' '

        update(proj, modules=modules_str, version=version, app_id=app_id)

        return 0

    if '--rollback' in args:
        update(proj, 'rollback', version=version, app_id=app_id)
        return 0

    elif '--dispatch' in args:
        update(proj, 'update_dispatch', '.', version=version, app_id=app_id)
        return 0

    elif '--indexes' in args:
        update(proj, 'update_indexes', '.', version=version, app_id=app_id)
        return 0

    elif '--queues' in args:
        update(proj, 'update_queues', '.', version=version, app_id=app_id)
        return 0

    elif '--cron' in args:
        update(proj, 'update_cron', '.', version=version, app_id=app_id)
        return 0

    update(proj, version=version, app_id=app_id)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

import os

if __name__ == '__main__':
    os.environ['MASHINA_SETTINGS_MODULE'] = '{{ project_name }}.config.settings'
    from mashina.commands import main

    main()

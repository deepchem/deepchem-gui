from argparse import ArgumentDefaultsHelpFormatter


def func(args, parser):
  # delay import of the module to improve performance
  import webbrowser
  from ..app import DEEPCHEM_GUI

  if args.browser:
    url = "http://%s:%s" % (args.host, args.port)
    webbrowser.open(url)

  DEEPCHEM_GUI.config['UPLOAD_FOLDER'] = args.dir
  DEEPCHEM_GUI.run(debug=args.debug, host=args.host, port=args.port)


def configure_parser(sub_parsers):
  help = 'Start a deepchem-gui server instance'
  p = sub_parsers.add_parser(
      'server',
      description=help,
      help=help,
      formatter_class=ArgumentDefaultsHelpFormatter)
  p.add_argument('-H', '--host', default="127.0.0.1", help='host', type=str)
  p.add_argument('-P', '--port', default=5000, help='port', type=int)
  p.add_argument(
      '-D',
      '--upload-dir',
      default='data/',
      dest='dir',
      help='uploaded file directory',
      type=str)
  p.add_argument('--debug', default=True, help='debug mode', type=bool)
  g = p.add_mutually_exclusive_group(required=False)
  g.add_argument(
      '--browser', action='store_true', default=True, help='launch browser')
  g.add_argument('--no-browser', action='store_false', dest='browser')

  p.set_defaults(func=func)

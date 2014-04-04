
import argparse, copy

desc = "Creates worklists (.gwl) for mutant pooling."
parser = argparse.ArgumentParser(description=desc, prog="pools2gwl")
parser.add_argument('plate',
                    help="plate number")
parser.add_argument('well',
                    help="well number")
parser.add_argument('--poolfile', dest='poolfile',
                    help="CSV file of pooling codes (plate,well,code)")
parser.add_argument('--gwlfile', dest='gwlfile',
                    help="template filename for output (.gwl) file")
parser.add_argument('--template', dest='template',
                    help="pipette command template; use {i} for well")
parser.add_argument('--debug', dest='debug', action='store_true',
                    help="enable debugging messages")

DEFAULTS = { 'poolfile' : 'codes.csv',
             'gwlfile' : 'pool{i}.gwl',
             'template' : 'put it in well {i}',
             'debug' : False }


def pool2gwl(plate, well, poolfile, gwlfile, template, debug):
   def show(string):
      if debug:
         print string

   key = "{plate},{well},".format(plate=plate, well=well)
   code = None
   with open(poolfile) as f:
      for line in f:
         if line.startswith(key):
            code = line.split(',')[2].rstrip()
            break
   if code is None:
      msg = "ERROR: no entry for plate {plate}, well {well}."
      print msg.format(plate=plate, well=well)
      return False

   show("")
   show("Key {plate},{well} mapped to code {code}".format(plate=plate,
                                                          well=well,
                                                          code=code))
   
   wells = [i+1 for i,b in enumerate(code) if b == '1']
   wells1 = wells[0:len(wells)//2]
   wells2 = wells[len(wells)//2:]

   def print_subpool(filename, wells):
      with open(filename, 'w') as f:
         show("File '{file}' contains wells {w}".format(file=filename,
                                                        w=wells))
         for i in wells:
            f.write(template.format(i=i) + "\n")

   print_subpool(gwlfile.format(i=1), wells1)
   print_subpool(gwlfile.format(i=2), wells2)

   show("")
   return True


if __name__ == '__main__':
   args = parser.parse_args()
   params = copy.copy(DEFAULTS)
   params['plate'] = args.plate
   params['well'] = args.well
   if args.poolfile:
      params['poolfile'] = args.poolfile
   if args.gwlfile:
      params['gwlfile'] = args.gwlfile
   if args.template:
      params['template'] = args.template
   if args.debug:
      params['debug'] = args.debug

   pool2gwl(**params)


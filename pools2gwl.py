
import argparse
import copy

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
parser.add_argument('--aspirate_template', dest='aspirate_template',
                    help=("aspirate command template; use {split}, " +
                          "{well}, and {volume}"))
parser.add_argument('--dispense_template', dest='dispense_template',
                    help="pipette command template; use {pool} and {volume}")
parser.add_argument('--volume', dest='volume',
                    help="despense volume for pools (ul)")
parser.add_argument('--debug', dest='debug', action='store_true',
                    help="enable debugging messages")

DEFAULTS = dict(poolfile='codes.csv',
                gwlfile='pool.gwl',
                aspirate_template=('draw {volume}ul from plate {split}, ' +
                                   'well {well}'),
                dispense_template='put {volume}ul in {pool}',
                volume=20,
                debug='False')


def pool2gwl(plate, well, poolfile, gwlfile, aspirate_template,
             dispense_template, volume, debug):
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
    show("key {plate},{well} mapped to code {code}".format(plate=plate,
                                                           well=well,
                                                           code=code))

    all_wells = [i+1 for i, b in enumerate(code) if b == '1']
    wells = [[], all_wells[0:len(all_wells)//2], all_wells[len(all_wells)//2:]]

    with open(gwlfile, 'w') as f:
        for split in [1, 2]:
            show("split {split} contains pools {w}".format(split=split,
                                                           w=wells[split]))
            vol = volume * len(wells[split])
            f.write(aspirate_template.format(split=split, well=well,
                                             volume=vol) + "\n")
            for i in wells[split]:
                f.write(dispense_template.format(pool=i, volume=volume) + "\n")

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
    if args.aspirate_template:
        params['aspirate_template'] = args.aspirate_template
    if args.dispense_template:
        params['dispense_template'] = args.dispense_template
    if args.volume:
        params['volume'] = float(args.volume)
    if args.debug:
        params['debug'] = args.debug

    pool2gwl(**params)

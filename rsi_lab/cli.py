import argparse
import json

from .evals.runner import evaluate_hidden, evaluate_policy
from .methods import aide2, dream_rsi, scientist2
from .problem.models import SceneBrief
from .problem.policies import Policy


def main():
    parser=argparse.ArgumentParser(description='RSI shot-planning codelabs')
    sub=parser.add_subparsers(dest='command',required=True)
    b=sub.add_parser('baseline'); b.add_argument('--scene',default='A detective enters a diner')
    d=sub.add_parser('dream-rsi'); d.add_argument('--rounds',type=int,default=3)
    a=sub.add_parser('aide2'); a.add_argument('--generations',type=int,default=3)
    s=sub.add_parser('scientist2'); s.add_argument('--budget',type=int,default=12)
    sub.add_parser('compare'); args=parser.parse_args()
    if args.command=='baseline':
        scene=SceneBrief(text=args.scene); policy=Policy(); print(json.dumps({'method':'baseline','plan':policy.plan(scene).model_dump(),'train':evaluate_policy(policy),'hidden':evaluate_hidden(policy)},indent=2))
    elif args.command=='dream-rsi': print(json.dumps(dream_rsi.run(args.rounds),indent=2))
    elif args.command=='aide2': print(json.dumps(aide2.run(args.generations),indent=2))
    elif args.command=='scientist2': print(json.dumps(scientist2.run(args.budget),indent=2))
    else:
        rows=[dream_rsi.run(3),aide2.run(3),scientist2.run(12)]
        print(json.dumps({'comparison':[{'method':r['method'],'train':r['train']['mean'],'hidden':r['hidden']['mean']} for r in rows]},indent=2))

if __name__=='__main__': main()
